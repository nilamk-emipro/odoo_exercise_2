# -*- coding: utf-8 -*-
{
    'name': 'Customer Details',
    'version': '1.1',
    'category': 'Utility',
    'author': 'Emipro Technologies Pvt. Ltd.',
    'description': """
    the module is for conduct exam
    """,
    'depends': ['sale', 'sales_team', 'crm', 'base'],
    'data': ['data/sequence_partner_lead_rel.xml',
             'views/partner_lead_rel.xml',
             'security/ir.model.access.csv'],
    'installable': True,
    'auto_install': False,
}
