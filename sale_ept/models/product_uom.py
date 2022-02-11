# -*- coding: utf-8 -*-

from odoo import fields, models

class ProductUOM(models.Model):

    _name = 'product.uom.ept'
    _description = 'Product Demo'

    name = fields.Char(string="Product Uom", help="Name of Product uom")
    uom_id = fields.Many2one(string="Product Category", comodel_name='product.uom.category.ept')

