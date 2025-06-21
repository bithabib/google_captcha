# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    recaptcha_v2_public_key = fields.Char("v2 Site Key", config_parameter='sot_google_recaptcha_v2.recaptcha_v2_public_key', groups='base.group_system')
    recaptcha_v2_private_key = fields.Char("v2 Secret Key", config_parameter='sot_google_recaptcha_v2.recaptcha_v2_private_key', groups='base.group_system')
