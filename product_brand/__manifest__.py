# -*- coding: utf-8 -*-
{
    'name': 'Product Brand',
    'version': '1.1',
    'category': 'Utility',
    'author': 'Emipro Technologies Pvt. Ltd.',
    'description': """
    the module is for exercise 2
    """,
    'depends': ['website', 'website_sale', 'product'],
    'data': ['views/product_brand_view.xml',
             'views/product_template_view.xml',
             'security/ir.model.access.csv'
             ],
    'installable': True,
    'auto_install': False,
}
