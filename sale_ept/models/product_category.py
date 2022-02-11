# -*- coding: utf-8 -*-

from odoo import fields, models

class ProductCategory(models.Model):

    _name = 'product.category.ept'
    _description = 'Product Demo'

    name = fields.Char(string="Product Category Name", help="Name of Product Category")
    parent_id = fields.Many2one(string="Product Category", comodel_name='product.category.ept')