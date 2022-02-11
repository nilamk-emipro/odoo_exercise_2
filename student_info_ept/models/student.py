# -*- coding: utf-8 -*-

from odoo import fields, models

class Student(models.Model):

    _name = 'student.ept'
    _description = 'Student Demo'

    name = fields.Char(string="Student Name", help="Name of Student", required=True)
    student_class = fields.Char(string="Class", help="Class", required=True)
    birthdate = fields.Date(string="BirthDate", help="Student's BirthDate", required=True)
    # course_ids = fields.Many2many('course.ept', 'student_course_rel',
    #                               'student_id',
    #                               'course_id',string='Students',help='Students'
    #                               )
    course_ids = fields.Many2many(string="Students",
                                  comodel_name='course.ept',
                                  relation='student_course_rel',
                                  column1='student_id',
                                  column2='course_id', help='Students')