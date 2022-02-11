# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockInventoryLine(models.Model):
    _name = 'stock.inventory.line.ept'
    _description = 'Stock Inventory Line'

    product_id = fields.Many2one(string="Product", comodel_name='product.ept', required=True)
    available_qty = fields.Float(string="System Quantity", help="System Available Quantity")
    counted_product_qty = fields.Float(string="Counted Product Quantity",
                                       help="Counted Product Quantity")
    inventory_id = fields.Many2one(string="Stock Inventory", comodel_name='stock.inventory.ept')
    difference = fields.Float(string="Difference", help="Difference", compute="compute_difference", store=False)

    @api.onchange('product_id')
    def on_change_product(self):
        if self.product_id:
            self.available_qty = self.product_id.with_context(location=self.inventory_id.location_id.id).product_stock

    @api.depends('available_qty','counted_product_qty')
    def compute_difference(self):
        for inventory_line in self:
            inventory_line.difference = inventory_line.counted_product_qty - inventory_line.available_qty