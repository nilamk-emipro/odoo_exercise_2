# -*- coding: utf-8 -*-

from odoo import fields, models,api

class CRMLeadLine(models.Model):

    _name = 'crm.lead.line.ept'
    _description = 'CRM Lead Line Demo'

    product_id = fields.Many2one(string="Product", comodel_name='product.ept')
    name = fields.Char(string="Description", help="Description")
    expected_sell_qty = fields.Float(string="Expected Sell Qty", help="Expected Sell Qty", digits=(6, 2))
    uom_id = fields.Many2one(string="UOM", help="UOM", comodel_name='product.uom.ept')
    lead_id = fields.Many2one(string="Lead", help="Lead", comodel_name='crm.lead.ept')

    @api.onchange('product_id')
    def on_change_partner(self):
        if self.product_id:
            self.name = self.product_id.name if self.product_id.description == False else self.product_id.description
            self.uom_id = self.product_id.uom_id