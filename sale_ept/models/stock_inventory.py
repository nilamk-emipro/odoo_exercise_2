# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError

class StockInventory(models.Model):

    _name = 'stock.inventory.ept'
    _description = 'Stock Inventory'

    name = fields.Char(string="Name", help="Name", required=True)
    state = fields.Selection([
        ('Draft', 'Draft'),
        ('InProgress', 'InProgress'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled')
    ], string='State', default='Draft')
    location_id = fields.Many2one(string="Stock Location", comodel_name='stock.location.ept')
    inventory_date = fields.Date(string="Inventory Date", help="Inventory Date", default=fields.Date.today)
    inventory_line_ids = fields.One2many(string="Inventory Line", comodel_name='stock.inventory.line.ept', inverse_name='inventory_id')
    stock_move_ids = fields.One2many(string="Stock Move", comodel_name='stock.move.ept', inverse_name='stock_inventory_id')

    def start_inventory(self):
        self.state = 'InProgress'

    def inventory_validate(self):
        self.state = 'Done'
        for line in self.inventory_line_ids:
            source_location_id = ''
            destination_location_id = ''

            if line.difference < 0:
                source_location_id = self.location_id.id
                destination_location_id = self.env['stock.location.ept'].search([('address_type', '=', 'Inventory Adjust')], limit=1).id
            elif line.difference != 0:
                source_location_id = self.env['stock.location.ept'].search([('address_type', '=', 'Inventory Adjust')], limit=1).id
                destination_location_id = self.location_id.id

            if source_location_id != '' and destination_location_id != '':
                stock_move_id = self.env['stock.move.ept'].create({
                    'name': line.product_id.name +' : ' +  str(self.env['stock.location.ept'].search([('address_type', '=', 'Inventory Adjust')], limit=1).name) + ' -> '+ str( self.location_id.name),
                    'product_id': line.product_id.id,
                    'uom_id': line.product_id.uom_id.id,
                    'source_location_id': source_location_id,
                    'destination_location_id': destination_location_id,
                    'qty_to_deliver': abs(line.difference),
                    'qty_done': abs(line.difference),
                    'state': 'Done',
                    'stock_inventory_id': self.id
                })

    @api.onchange('state')
    def on_change_state(self):
        if self.state == 'Cancelled':
            if self.env['stock.inventory.ept'].search([('id', '=', self._origin.id)]).state != 'Done':
                self.state = 'Cancelled'
            else:
                raise ValidationError("Can't Cancel the Inventory All Ready Done")
