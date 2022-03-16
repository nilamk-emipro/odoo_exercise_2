# -*- coding: utf-8 -*-

from odoo import fields, models, api

class SalesPerson(models.TransientModel):
    _name = 'sales.person'
    _description = 'Sales person'

    from_date = fields.Date(string="From Date", help="From Date", default=fields.Date.today)
    to_date = fields.Date(string="To Date", help="To Date", default=fields.Date.today)
    sale_person_id = fields.Many2one(string="Sales Person", comodel_name='res.users')

    def print_report(self):
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'sale_person_id': self.sale_person_id
        }
        return self.env.ref('sale_order_extended.action_report_sale_order_for_sales_person').report_action(self, data=data)

