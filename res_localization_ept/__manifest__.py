# -*- coding: utf-8 -*-
{
    'name': 'Country demo 2',
    'version': '1.1',
    'category': 'Utility',
    'author': 'Emipro Technologies Pvt. Ltd.',
    'description': """
    the module is for exercise 2
    """,
    'depends': ['base'],
    'data': ['views/country.xml',
             'views/states.xml',
             'views/city.xml',
             'security/country_security.xml',
             'security/state_security.xml',
             'security/city_security.xml',
             'security/ir.model.access.csv'],
    'installable': True,
    'auto_install': False,
}
