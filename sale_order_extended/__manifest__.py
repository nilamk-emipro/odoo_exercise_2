# -*- coding: utf-8 -*-
{
    'name': 'Sale CRM Modification',
    'version': '1.1',
    'category': 'Utility',
    'author': 'Emipro Technologies Pvt. Ltd.',
    'description': """
    the module is for exercise 2
    """,
    'depends': ['sale_crm', 'product'],
    'data': ['views/sale_order.xml',
             'views/product_product.xml',
             'views/sale_order_line.xml',
             'data/crm_lead_tag_data.xml',
             'data/product_data.xml',
             'wizard/merge_orders.xml',
             'security/ir.model.access.csv',
             ],
    'installable': True,
    'auto_install': False,
}
