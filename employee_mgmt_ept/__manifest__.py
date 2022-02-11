# -*- coding: utf-8 -*-
{
    'name': 'Employee Management',
    'version': '1.1',
    'category': 'Utility',
    'author': 'Emipro Technologies Pvt. Ltd.',
    'description': """
    the module is for exercise 2
    """,
    'depends': ['base'],
    'data': ['views/department_view.xml',
             'views/shift_view.xml',
             'views/employee_view.xml',
             'views/leave.xml',
             'security/department_security.xml',
             'security/shift_security.xml',
             'security/employee_security.xml',
             'security/leave_security.xml',
             'security/ir.model.access.csv'
             ],
    'installable': True,
    'auto_install': False,
}
