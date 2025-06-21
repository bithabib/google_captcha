# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Google reCAPTCHA V2 integration',
    'category': 'Signup',
    'version': '16.0.1',
    'description': """
This module implements reCaptchaV2 so that you can prevent bot spam on your public modules.
    """,
    'author': "School of Thought",
    'maintainer': "School of Thought",
    'price': '5.00',
    'currency': 'USD',
    'website': "https://schoolofthought.tech",
    'license': 'AGPL-3',
    # 'depends': ['auth_signup', 'google_recaptcha'],
    'data': [
        'views/res_config_settings_view.xml',
        'views/recaptcha_form_template.xml',
    ],
    'license': 'LGPL-3',
}
# -*- coding: utf-8 -*-
# {
#     'name': "Signup Email Verification",

#     'summary': "Signup Email Verification",

#     'description': """ Signup Email Verification is where you can verify your email address after signup bu sending an verification code.""",

#     'author': "School of Thought",
#     'maintainer': "School of Thought",
#     'price': '5.00',
#     'currency': 'USD',
#     'website': "https://schoolofthought.tech",
#     'license': 'AGPL-3',
#     'category': 'Signup',
#     'version': '14.0.1',
#     'depends': ['base', 'mail'],
#     'data': [
#         'views/views.xml',
#         'views/templates.xml',
#         'data/signup_verification_email_teplate.xml',
        
#     ],
#     'images': ['static/description/banner.png', 'static/description/icon.png'],
# }
