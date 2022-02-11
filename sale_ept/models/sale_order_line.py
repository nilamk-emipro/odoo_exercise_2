# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _name = 'sale.order.line.ept'
    _description = 'Sale Order Line Demo'

    order_no_id = fields.Many2one(string="Order No", comodel_name='sale.order.ept')
    product_id = fields.Many2one(string="Product", comodel_name='product.ept')
    name = fields.Text(string="Description", help="Description")
    quantity = fields.Float(string="Quantity", help="Quantity", digits=(6, 2))
    unit_price = fields.Float(string="Unit Price", help="Unit Price", digits=(6, 2))
    state = fields.Selection([
        ('Draft', 'Draft'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled')
    ], string='State', default='Draft')
    uom_id = fields.Many2one(string="UOM", comodel_name='product.uom.ept')
    subtotal_without_tax = fields.Float(string="Sub Total", help="SubTotal", compute="compute_subtotal", store=True)
    stock_move_ids = fields.One2many(string="Stock Move", comodel_name='stock.move.ept', inverse_name='sale_line_id',
                                     readonly=True)
    delivered_qty = fields.Float(string="Delivered Qty", help="Delivered Qty", compute="compute_delivered_qty",
                                 store=False)
    cancelled_qty = fields.Float(string="Cancelled Qty", help="Cancelled Qty", compute="compute_delivered_qty",
                                 store=False)
    warehouse_id = fields.Many2one(string="Warehouse", comodel_name='stock.warehouse.ept')

    @api.onchange('product_id')
    def on_change_product(self):
        if self.product_id:
            self.unit_price = self.product_id.sale_price
            self.quantity = 1
            self.name = self.product_id.name

    @api.depends('quantity', 'unit_price')
    def compute_subtotal(self):
        for order_line in self:
            order_line.subtotal_without_tax = order_line.quantity * order_line.unit_price

    def compute_delivered_qty(self):
        for order_line in self:
            total_del_qty = 0
            total_cancel_qty = 0
            for move_line in self.env['stock.move.ept'].search([('sale_line_id', '=', order_line.id)]):
                if move_line.state == 'Done':
                    total_del_qty += move_line.qty_done
                if move_line.state == 'Cancelled':
                    total_cancel_qty += move_line.qty_done
            order_line.delivered_qty = total_del_qty
            order_line.cancelled_qty = total_cancel_qty
