# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import requests

from odoo import api, models, _
from odoo.http import request
from odoo.exceptions import UserError, ValidationError

from odoo.addons.web.controllers.home import SIGN_UP_REQUEST_PARAMS

SIGN_UP_REQUEST_PARAMS.add('g-recaptcha-response')

logger = logging.getLogger(__name__)


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        session_info = super().session_info()
        return self._add_public_key_to_session_info(session_info)

    @api.model
    def get_frontend_session_info(self):
        frontend_session_info = super().get_frontend_session_info()
        return self._add_public_key_to_session_info(frontend_session_info)

    @api.model
    def _add_public_key_to_session_info(self, session_info):
        """Add the ReCaptcha public key to the given session_info object"""
        public_key = self.env['ir.config_parameter'].sudo().get_param(
            'sot_google_recaptcha_v2.recaptcha_v2_public_key')
        if public_key:
            session_info['recaptcha_v2_public_key'] = public_key
        return session_info

    @api.model
    def _verify_request_recaptcha_token(self, action):
        """ Verify the recaptcha token for the current request.
            If no recaptcha private key is set the recaptcha verification
            is considered inactive and this method will return True.
        """
        res = super()._verify_request_recaptcha_token(action)
        logger.info("Recaptcha verification result for action '%s': %s", action, res)

        if not res:  # check result of google_recaptcha
            return res

        ip_addr = request.httprequest.remote_addr
        token = request.params.pop('g-recaptcha-response', False)
        recaptcha_result = request.env['ir.http']._verify_recaptcha_v2_token(ip_addr, token)
        logger.info("Recaptcha verification result for recaptcha_v2_result '%s': %s", action, recaptcha_result)

        if recaptcha_result in ['is_human', 'no_secret']:
            return True
        if recaptcha_result == 'wrong_secret':
            raise ValidationError(_("The recaptcha private key is invalid."))
        elif recaptcha_result == 'wrong_token':
            raise ValidationError(_("The recaptcha human validation failed."))
        elif recaptcha_result == 'timeout':
            raise UserError(_("Your request has timed out, please retry."))
        elif recaptcha_result == 'bad_request':
            raise UserError(_("The request is invalid or malformed."))
        else:  # wrong_action e.g.
            return False

    @api.model
    def _verify_recaptcha_v2_token(self, ip_addr, token):
        """
            Verify a recaptchaV2 token and returns the result as a string.
            RecaptchaV2 verify DOC: https://developers.google.com/recaptcha/docs/verify

            :return: The result of the call to the google API:
                     is_human: The token is valid and the user trustworthy.
                     is_bot: The user is not trustworthy and most likely a bot.
                     no_secret: No reCaptcha secret set in settings.
                     wrong_action: the action performed to obtain the token does not match the one we are verifying.
                     wrong_token: The token provided is invalid or empty.
                     wrong_secret: The private key provided in settings is invalid.
                     timeout: The request has timout or the token provided is too old.
                     bad_request: The request is invalid or malformed.
            :rtype: str
        """
        private_key = request.env['ir.config_parameter'].sudo().get_param(
            'sot_google_recaptcha_v2.recaptcha_v2_private_key'
        )
        if not private_key:
            return 'no_secret'

        try:
            r = requests.post('https://www.recaptcha.net/recaptcha/api/siteverify', {
                'secret': private_key,
                'response': token,
                'remoteip': ip_addr,
            }, timeout=2)  # it takes ~50ms to retrieve the response
            result = r.json()
            res_success = result['success']
        except requests.exceptions.Timeout:
            logger.error("Trial captcha verification timeout for ip address %s", ip_addr)
            return 'timeout'
        except Exception:
            logger.error("Trial captcha verification bad request response")
            return 'bad_request'

        if res_success:
            return 'is_human'

        errors = result.get('error-codes', [])
        logger.warning(
            "Trial captcha verification for ip address %s failed error codes %r. token was: [%s]",
            ip_addr, errors, token
        )
        for error in errors:
            if error in ['missing-input-secret', 'invalid-input-secret']:
                return 'wrong_secret'
            if error in ['missing-input-response', 'invalid-input-response']:
                return 'wrong_token'
            if error == 'timeout-or-duplicate':
                return 'timeout'
            if error == 'bad-request':
                return 'bad_request'
        return 'is_bot'
