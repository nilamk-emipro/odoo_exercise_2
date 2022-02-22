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
    subtotal_without_tax = fields.Float(string="Sub Total", help="SubTotal", compute="compute_subtotal_without_tax", store=True)
    stock_move_ids = fields.One2many(string="Stock Move", comodel_name='stock.move.ept', inverse_name='sale_line_id',
                                     readonly=True)
    delivered_qty = fields.Float(string="Delivered Qty", help="Delivered Qty", compute="compute_delivered_qty",
                                 store=False)
    cancelled_qty = fields.Float(string="Cancelled Qty", help="Cancelled Qty", compute="compute_delivered_qty",
                                 store=False)
    warehouse_id = fields.Many2one(string="Warehouse", comodel_name='stock.warehouse.ept')
    tax_ids = fields.Many2many(string="Customer Taxes", help="Tax", comodel_name='account.tax.ept', domain=[('tax_use', '=', 'Sales')])
    subtotal_with_tax = fields.Float(string="Sub Total With Tax", help="SubTotalWithTax", compute="compute_subtotal_with_tax", store=True)

    @api.onchange('product_id')
    def on_change_product(self):
        if self.product_id:
            self.unit_price = self.product_id.sale_price
            self.quantity = 1
            self.name = self.product_id.name
            self.tax_ids = self.product_id.tax_ids

    @api.depends('quantity', 'unit_price')
    def compute_subtotal_without_tax(self):
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

    @api.depends('quantity', 'unit_price', 'tax_ids', 'product_id')
    def compute_subtotal_with_tax(self):
        for order_line in self:
            tax_amount = 0
            for tax_id in self.tax_ids:
                if tax_id.tax_amount_type == 'Percentage':
                    tax_amount += (order_line.subtotal_without_tax * tax_id.tax_value) / 100
                else:
                    tax_amount += tax_id.tax_value
            order_line.subtotal_with_tax = order_line.subtotal_without_tax + tax_amount
