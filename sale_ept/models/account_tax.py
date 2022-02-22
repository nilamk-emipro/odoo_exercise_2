# -*- coding: utf-8 -*-

from odoo import fields, models

class AccountTax(models.Model):

    _name = 'account.tax.ept'
    _description = 'Account Tax'

    name = fields.Char(string="Name", help="Name")
    tax_use = fields.Selection(selection=[('None', 'None'), ('Sales', 'Sales'), ('Purchase', 'Purchase')])
    tax_value = fields.Float(string="Amount", help="Tax Amount")
    tax_amount_type = fields.Selection(selection=[('Percentage', 'Percentage'), ('Fixed', 'Fixed')],default='Percentage')
