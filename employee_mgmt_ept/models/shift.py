# -*- coding: utf-8 -*-

from odoo import fields, models

class Shift(models.Model):

    _name = 'employee.department.shift.ept'
    _description = 'Shift Demo'
    _rec_name = 'shift'

    shift = fields.Selection(selection=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('Night', 'Night')])
    employee_ids = fields.One2many(string="Employee", comodel_name='employee.ept', inverse_name='shift_id')
