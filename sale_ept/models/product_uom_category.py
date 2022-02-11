# -*- coding: utf-8 -*-

from odoo import fields, models

class ProductUOMCategory(models.Model):

    _name = 'product.uom.category.ept'
    _description = 'Product Demo'

    name = fields.Char(string="Product uom Category Name", help="Name of Product uom Category")
    uom_ids = fields.One2many(string="Product Category", comodel_name='product.uom.ept', inverse_name='uom_id')

