# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    order_line_child_id = fields.Many2one(comodel_name='sale.order.line', string="Child Deposit",
                                          help='Sale Order Line id for reference of Deposit')
    order_line_parent_id = fields.One2many(comodel_name='sale.order.line', inverse_name='order_line_child_id')
    order_line_profit_value = fields.Float(string="Profit Value", help="Profit Value",compute='compute_calculate_profit')
    order_line_profit_percentage = fields.Float(string="Profit Percentage", help="Profit Percentage",compute='compute_calculate_profit')
    order_line_cost_price = fields.Float(string="Cost Price", help="Cost Price", readonly=True, copy=False)
    add_warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='Warehouse')

    @api.depends('price_unit')
    def compute_calculate_profit(self):
        for line in self:
            line.order_line_profit_value = line.price_subtotal - (line.order_line_cost_price * line.product_uom_qty)
            total_profit = (line.product_id.list_price * line.product_uom_qty) - (
                    line.product_id.standard_price * line.product_uom_qty)
            line.order_line_profit_percentage = (line.order_line_profit_value * 100) / 1 if total_profit==0 else total_profit

    @api.onchange('price_unit')
    def onchange_product_id(self):
        self.order_line_cost_price = 1 if self.product_id.standard_price == 0 else self.product_id.standard_price

    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        # if self.add_warehouse_id:
        #     values.update({
        #         'warehouse_id': self.add_warehouse_id
        #     })
        return values