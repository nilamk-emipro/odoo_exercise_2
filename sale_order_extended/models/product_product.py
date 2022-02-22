# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class ProductProduct(models.Model):
    _inherit = 'product.product'

    deposit_product_id = fields.Many2one(comodel_name='product.product', string='Deposit Product')
    deposit_product_qty = fields.Float(string='Deposit Product Qty', help='Deposit Quantity')
