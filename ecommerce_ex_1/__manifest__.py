# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'eCommerce Demo',
    'category': 'Website/Website',
    'sequence': 50,
    'summary': 'Practice JS',
    'version': '1.1',
    'description': "",
    'depends': ['web', 'website', 'sale', 'website_payment', 'website_mail', 'portal_rating', 'digest'],
    'data': [
        'views/custom_page.xml',
        'views/product_page.xml'
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_frontend': [
            'ecommerce_ex_1/static/src/js/product_data.js',
        ],
    }
}
