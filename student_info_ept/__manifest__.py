# -*- coding: utf-8 -*-
{
    'name': 'Student Info',
    'version': '1.1',
    'category': 'Utility',
    'author': 'Emipro Technologies Pvt. Ltd.',
    'description': """
    the module is for exercise 2
    """,
    'depends': ['sales_team'],
    'data': ['views/student_view.xml',
             'views/course_view.xml',
             'security/student_security.xml',
             'security/course_security.xml',
             'security/ir.model.access.csv'],
    'installable': True,
    'auto_install': False,
}
