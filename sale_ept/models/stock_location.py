# -*- coding: utf-8 -*-

from odoo import fields, models

class StockLocation(models.Model):

    _name = 'stock.location.ept'
    _description = 'Stock Location'

    name = fields.Char(string="Name", help="Name", required=True)
    parent_id = fields.Many2one(string="Parent", comodel_name='stock.location.ept')
    address_type = fields.Selection(
        selection=[('Vendor', 'Vendor'),
                   ('Customer', 'Customer'),
                   ('Internal', 'Internal'),
                   ('Inventory Adjust', 'Inventory Adjust'),
                   ('Production', 'Production'),
                   ('Transit', 'Transit'),
                   ('View', 'View'),
                   ])
    is_scrap_location = fields.Boolean(string="Scrap Location", help="This Location is Scrap Location or Not")

