# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Demo JS',
    'category': 'Website/Website',
    'sequence': 50,
    'summary': 'Practice JS',
    'version': '1.1',
    'description': "",
    'depends': ['website', 'sale', 'website_payment', 'website_mail', 'portal_rating', 'digest'],
    'data': [
        'views/assets.xml',
    ],
    'qweb': ['static/src/xml/demo_template.xml'],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'website_demo_test/static/src/js/demo1.js',
        ],
    },
    'license': 'LGPL-3',
}
