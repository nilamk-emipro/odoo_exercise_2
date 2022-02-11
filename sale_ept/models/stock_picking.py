# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _name = 'stock.picking.ept'
    _description = 'Stock Picking'

    name = fields.Char(string="Name", help="Name", index=True, default=lambda self: _('New'))
    partner_id = fields.Many2one(string="Partner", comodel_name='res.partner.ept')
    state = fields.Selection([
        ('Draft', 'Draft'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled')
    ], string='State', default='Draft')
    sale_order_id = fields.Many2one(string="Sale Order", comodel_name='sale.order.ept')
    purchase_order_id = fields.Many2one(string="Purchase Order", comodel_name='purchase.order.ept')
    transaction_type = fields.Selection(selection=[('In', 'In'), ('Out', 'Out')])
    move_ids = fields.One2many(string="Move", comodel_name='stock.move.ept', inverse_name='picking_id')
    transaction_date = fields.Date(string="Transaction Date", help="Transaction Date", default=fields.Date.today)
    back_order_id = fields.Many2one(string="Back Order", comodel_name='stock.picking.ept')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if vals.get('transaction_type') == 'In':
                vals['name'] = self.env['ir.sequence'].next_by_code('stock.picking.in') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('stock.picking.out') or _('New')
        result = super(StockPicking, self).create(vals)
        return result

    def validate(self):
        stock_move_line = []
        total_done_qty = 0
        for move_id in self.move_ids:
            if move_id.qty_done != 0:
                if move_id.qty_to_deliver != move_id.qty_done:
                    stock_move_line.append(
                        (0, 0, {
                            'name': move_id.name,
                            'product_id': move_id.product_id.id,
                            'uom_id': move_id.uom_id.id,
                            'source_location_id': move_id.source_location_id.id,
                            'destination_location_id': move_id.destination_location_id.id,
                            'qty_to_deliver': move_id.qty_to_deliver - move_id.qty_done,
                            'qty_done': 0,
                            'sale_line_id': move_id.sale_line_id.id
                        })
                    )
                    move_id.qty_to_deliver = move_id.qty_done
                    total_done_qty += move_id.qty_done
            else:
                stock_move_line.append(
                    (2, move_id.id, 0)
                )
                stock_move_line.append(
                    (0, 0, {
                        'name': move_id.name,
                        'product_id': move_id.product_id.id,
                        'uom_id': move_id.uom_id.id,
                        'source_location_id': move_id.source_location_id.id,
                        'destination_location_id': move_id.destination_location_id.id,
                        'qty_to_deliver': move_id.qty_to_deliver,
                        'qty_done': 0,
                        'sale_line_id': move_id.sale_line_id.id
                    })
                )
            move_id.state = 'Done'
        if total_done_qty != 0:
            stock_picking_id = self.env['stock.picking.ept'].create({
                'partner_id': self.partner_id.id,
                'sale_order_id': self.sale_order_id.id,
                'transaction_type': self.transaction_type,
                'move_ids': stock_move_line,
                'back_order_id': self.id
            })
        else:
            raise ValidationError("At least add done qty of one product")

        self.state = 'Done'
