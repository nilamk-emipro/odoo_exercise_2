# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    order_line_child_id = fields.Many2one(comodel_name='sale.order.line', string="Child Deposit", help='Sale Order Line id for reference of Deposit')
    order_line_parent_id = fields.One2many(comodel_name='sale.order.line', inverse_name='order_line_child_id')
