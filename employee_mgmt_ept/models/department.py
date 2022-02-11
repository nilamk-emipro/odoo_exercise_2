# -*- coding: utf-8 -*-

from odoo import fields, models

class Department(models.Model):

    _name = 'employee.department.ept'
    _description = 'Department Demo'

    name = fields.Char(string="Department Name", help="Name of Department")
    employee_ids = fields.One2many(string="Employee", comodel_name='employee.ept', inverse_name='employee_department_id')
    department_manager_id = fields.Many2one(string="Department Manager", comodel_name='res.users')