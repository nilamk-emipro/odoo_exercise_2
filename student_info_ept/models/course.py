# -*- coding: utf-8 -*-

from odoo import fields, models

class Course(models.Model):

    _name = 'course.ept'
    _description = 'Course Demo'

    name = fields.Char(string="Course Name", help="Course Name",required=True)
    # student_ids = fields.Many2many('student.ept', 'student_course_rel',
    #                                'course_id','student_id',string='Courses',help='Courses')
    student_ids = fields.Many2many(string="Course",
                                  comodel_name='student.ept',
                                  relation='student_course_rel',
                                  column1='course_id',
                                  column2='student_id', help='Courses')
