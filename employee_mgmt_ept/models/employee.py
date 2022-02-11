# -*- coding: utf-8 -*-

from odoo import fields, models

class Employee(models.Model):

    _name = 'employee.ept'
    _description = 'Employee Demo'

    name = fields.Char(string="Employee Name", help="Name of Employee", required=True)

    employee_department_id = fields.Many2one(string="Department", comodel_name='employee.department.ept')

    shift_id = fields.Many2one(string="Shift", comodel_name='employee.department.shift.ept', required=True)
    job_position = fields.Char(string="Job Position of Employee", help="Job Position of Employee")
    salary = fields.Float(string="Salary", help="Employee's Salary", digits=(6, 2))
    hire_date = fields.Date(string="Hire Date", help="Hire Date of Employee")
    gender = fields.Selection(selection=[('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender')])
    job_type = fields.Selection(selection=[('Permanent', 'Permanent'), ('Ad_Hoc', 'Ad_Hoc')])
    is_manager = fields.Boolean(string="Is Manager", help="Employee is Manager Or Not")
    manager_id = fields.Many2one(string="Manager", comodel_name='employee.ept', domain=[('is_manager', '=', True)])
    related_user = fields.Many2one(string="Related User", comodel_name='res.users')
    # employee_ids = fields.One2many(string="Employee", comodel_name='employee.ept', inverse_name='employee_id')
    increment_percentage = fields.Float(string="Increment Percentage", help="Employee's Increment Percentage", digits=(6, 2))
