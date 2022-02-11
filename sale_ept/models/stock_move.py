# -*- coding: utf-8 -*-

from odoo import fields, models

class StockMove(models.Model):
    _name = 'stock.move.ept'
    _description = 'Stock Move'

    name = fields.Char(string="Description", help="Name")
    product_id = fields.Many2one(string="Product", comodel_name='product.ept')
    uom_id = fields.Many2one(string="UOM", comodel_name='product.uom.ept')
    source_location_id = fields.Many2one(string="Stock Location", comodel_name='stock.location.ept')
    destination_location_id = fields.Many2one(string="Destination Location", comodel_name='stock.location.ept')
    qty_to_deliver = fields.Float(string="Demand", help="Qty to Deliver", readonly=True)
    qty_done = fields.Float(string="Done Quantity", help="Done Quantity")
    state = fields.Selection([
        ('Draft', 'Draft'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled')
    ], string='State', default='Draft')
    sale_line_id = fields.Many2one(string="Sale Order Line", comodel_name='sale.order.line.ept')
    purchase_line_id = fields.Many2one(string="Purchase Order Line", comodel_name='purchase.order.line.ept')
    stock_inventory_id = fields.Many2one(string="Stock Inventory", comodel_name='stock.inventory.ept')
    picking_id = fields.Many2one(string="Stock Picking", comodel_name='stock.picking.ept')


