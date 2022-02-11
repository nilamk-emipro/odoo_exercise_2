# -*- coding: utf-8 -*-

from odoo import fields, models

class StockWarehouse(models.Model):

    _name = 'stock.warehouse.ept'
    _description = 'Stock Warehouse'

    name = fields.Char(string="Name", help="Name of Warehouse", required=True)
    short_code = fields.Char(string="Short Code", help="Short Code of Warehouse", required=True)
    address_id = fields.Many2one(string="Address", comodel_name='res.partner.ept')
    stock_location_id = fields.Many2one(string="Stock Location", comodel_name='stock.location.ept', domain=[('address_type', '=', 'Internal')])
    # , ('parent_id', '!=', False)]
    view_location_id = fields.Many2one(string="View Location", comodel_name='stock.location.ept', domain=[('address_type', '=', 'View')])
