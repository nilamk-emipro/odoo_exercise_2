# -*- coding: utf-8 -*-

from odoo import fields, models

class PurchaseOrderLine(models.Model):

    _name = 'purchase.order.line.ept'
    _description = 'Purchase Order Line'

    order_no_id = fields.Many2one(string="Order No", comodel_name='purchase.order.ept')
    product_id = fields.Many2one(string="Product", comodel_name='product.ept')
    name = fields.Text(string="Description", help="Description")
    quantity = fields.Float(string="Quantity", help="Quantity", digits=(6, 2))
    cost_price = fields.Float(string="Cost Price", help="Cost Price", digits=(6, 2))
    state = fields.Selection([
        ('Draft', 'Draft'),
        ('Confirmed', 'Confirmed'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled')
    ], string='State', default='Draft')
    uom_id = fields.Many2one(string="UOM", comodel_name='product.uom.ept')
