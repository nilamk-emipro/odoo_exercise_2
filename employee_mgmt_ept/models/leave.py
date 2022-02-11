# -*- coding: utf-8 -*-

from odoo import fields, models


class Shift(models.Model):
    _name = 'employee.leave.ept'
    _description = 'Leave Demo'

    employee_id = fields.Many2one(string="Employee", comodel_name='employee.ept')
    department_id = fields.Many2one(string="Department", comodel_name='employee.department.ept', related='employee_id.employee_department_id', readonly=True)
    start_date = fields.Date(string="Start Date", help="Start Date")
    end_date = fields.Date(string="End Date", help="End Date")
    status = fields.Selection([
        ('Draft', 'Draft'),
        ('Approved', 'Approved'),
        ('Refused', 'Refused'),
        ('Cancelled', 'Cancelled')
    ], string='Status', default='Draft', tracking=True)
    leave_description = fields.Char(string="Leave Description", help="Leave Description", required=True)
