# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductStockUpdate(models.Model):
    _name = 'product.stock.update.ept'
    _description = 'Product Stock Update'

    location_id = fields.Many2one(string="Location", comodel_name='stock.location.ept')
    available_stock = fields.Float(string="Available Stock", help="Available Stock")
    counted_qty = fields.Float(string="Counted Qty", help="Counted Stock")
    difference_qty = fields.Float(string="Difference Qty", help="Difference", compute="compute_difference", store=False)

    @api.depends('available_stock', 'counted_qty')
    def compute_difference(self):
        self.difference_qty = self.counted_qty - self.available_stock

    @api.onchange('location_id')
    def on_change_product(self):
        product_ids = self.env.context.get('active_ids')
        self.available_stock = self.env['product.ept'].with_context(location=self.location_id.id).browse(
            product_ids[0]).product_stock

    def update_stock(self):
        stock_inventory_id = self.env['stock.inventory.ept'].create({
            'name': 'Inventory_from_stock_update',
            'location_id': self.location_id.id,
            'inventory_date': fields.Date.today()
        })

        self.env['stock.inventory.line.ept'].create({
            'product_id': self.env.context.get('active_ids')[0],
            'available_qty': self.available_stock,
            'counted_product_qty': self.counted_qty,
            'inventory_id': stock_inventory_id.id
        })

        stock_inventory_id.inventory_validate()