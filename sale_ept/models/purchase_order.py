# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _name = 'purchase.order.ept'
    _description = 'Purchase Order'

    name = fields.Char(name="Order Number", help="Purchase Order Number", index=True, default=lambda self: _('New'))
    warehouse_id = fields.Many2one(string="Warehouse", comodel_name='stock.warehouse.ept')
    partner_id = fields.Many2one(string="Vendor", comodel_name='res.partner.ept')
    order_date = fields.Date(string="Order Date", help="Date of Order")
    state = fields.Selection([
        ('Draft', 'Draft'),
        ('Confirm', 'Confirm'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled')
    ], string='State', default='Draft')
    purchase_order_line_ids = fields.One2many(string="Order Line", comodel_name='purchase.order.line.ept',
                                              inverse_name='order_no_id')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order.ept') or _('New')
        result = super(PurchaseOrder, self).create(vals)
        return result

    def order_confirm(self):
        if self.warehouse_id:
            stock_move_line = []
            for order_line in self.purchase_order_line_ids:
                stock_move_line.append(
                    (0, 0, {
                        'name': order_line.product_id.name +' : ' +
                                str(self.env['stock.location.ept'].search([('address_type', '=', 'Vendor')], limit=1).name) + ' -> '+
                                str(self.warehouse_id.name),
                        'product_id': order_line.product_id.id,
                        'uom_id': order_line.uom_id.id,
                        'source_location_id': self.env['stock.location.ept'].search(
                                [('address_type', '=', 'Vendor')], limit=1).id,
                        'destination_location_id': self.warehouse_id.stock_location_id.id,
                        'qty_to_deliver': order_line.quantity,
                        'qty_done': 0,
                        'purchase_line_id': order_line.id
                    })
                )

            stock_picking_id = self.env['stock.picking.ept'].create({
                'name': self.name,
                'partner_id': self.partner_id.id,
                'purchase_order_id': self.id,
                'transaction_type': 'In',
                'move_ids': stock_move_line
            })
        else:
            raise ValidationError("Location Not Found")
