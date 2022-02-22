# -*- coding: utf-8 -*-
{
    'name': 'Product Management',
    'version': '1.1',
    'category': 'Utility',
    'author': 'Emipro Technologies Pvt. Ltd.',
    'description': """
    the module is for exercise 2
    """,
    'depends': ['base', 'res_localization_ept'],
    'data': ['views/product_category.xml',
             'views/product_uom_category.xml',
             'views/product_uom.xml',
             'views/product.xml',
             'views/partner.xml',
             'data/seq_sale_order.xml',
             'views/sale_order_line.xml',
             'views/sale_order.xml',
             'views/crm_team.xml',
             'views/crm_lead.xml',
             'views/stock_location.xml',
             'views/stock_warehouse.xml',
             'views/stock_picking.xml',
             'views/stock_move.xml',
             'data/seq_purchase_order.xml',
             'views/purchase_order.xml',
             'views/purchase_order_line.xml',
             'views/stock_inventory.xml',
             'views/stock_inventory_line.xml',
             'views/product_stock_update.xml',
             'wizard/product_stock_update_ept.xml',
             'views/account_tax.xml',
             'security/sale_order_security.xml',
             'security/ir.model.access.csv',
             'data/sequence_stock_picking.xml',
             ],
    'installable': True,
    'auto_install': False,
}
