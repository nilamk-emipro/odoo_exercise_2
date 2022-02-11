# -*- coding: utf-8 -*-
import dateutil.utils
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _name = 'sale.order.ept'
    _description = 'Sale Order Demo'

    name = fields.Char(string="Order No", help="Order No", index=True, default=lambda self: _('New'))
    partner_id = fields.Many2one(string="Partner", comodel_name='res.partner.ept', domain="[('parent_id','=',False)]")
    partner_invoice_id = fields.Many2one(string="Partner Invoice", comodel_name='res.partner.ept',
                                         domain="[('address_type','=','Invoice'),('parent_id','=',partner_id)]")
    partner_shipping_id = fields.Many2one(string="Partner Shipping", comodel_name='res.partner.ept',
                                          domain="[('address_type','=','Shipping'),('parent_id','=',partner_id)]")
    sale_order_date = fields.Date(string="Sale Order Date", help="Date of Sale Order", default=fields.Date.today)
    order_line_ids = fields.One2many(string="Order Lines", comodel_name='sale.order.line.ept',
                                     inverse_name='order_no_id')
    sales_persons = fields.Many2one(string="Sales Persons", comodel_name='res.users')
    state = fields.Selection([
        ('Draft', 'Draft'),
        ('Confirmed', 'Confirmed'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled')
    ], string='State', default='Draft')
    total_weight = fields.Float(string="Total Weight", help="Total Weight", digits=(6, 2),
                                compute="compute_total_weight", store=False)
    total_volume = fields.Float(string="Total Volume", help="Total Volume", digits=(6, 2),
                                compute="compute_total_volume", store=False)
    order_total = fields.Float(string="Total", help="Total", digits=(6, 2),
                               compute="compute_total", store=True)
    lead_id = fields.Many2one(string="Lead", comodel_name='crm.lead.ept')
    warehouse_id = fields.Many2one(string="Stock Warehouse", comodel_name='stock.warehouse.ept')
    picking_ids = fields.One2many(string="Picking", comodel_name='stock.picking.ept', inverse_name='sale_order_id',
                                  readonly=True)
    delivery_order_count = fields.Float(compute="compute_delivery_order_count", store=False)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.order.ept') or _('New')
        result = super(SaleOrder, self).create(vals)
        return result

    @api.depends('order_line_ids')
    def compute_total_weight(self):
        for order in self:
            product_weight = 0
            for line in order.order_line_ids:
                product_weight = product_weight + (line.quantity * line.product_id.weight)
            order.total_weight = product_weight

    @api.depends('order_line_ids')
    def compute_total_volume(self):
        for order in self:
            product_volume = 0
            for line in order.order_line_ids:
                product_volume = product_volume + (line.quantity * line.product_id.volume)
            order.total_volume = product_volume

    @api.depends('order_line_ids')
    def compute_total(self):
        total = 0
        for order in self.order_line_ids:
            total = total + order.subtotal_without_tax
        self.order_total = total

    @api.onchange('partner_id')
    def on_change_partner(self):
        if self.partner_id:
            # self.partner_invoice_id = self.partner_id.search(
            #     [('parent_id', '=', self.partner_id.id),
            #      ('address_type', '=', 'Invoice')], limit=1)

            self.partner_invoice_id = self.partner_id if self.partner_id.child_ids.filtered(
                lambda child_id: child_id.address_type == 'Invoice').ids == [] else self.partner_id.child_ids.filtered(
                lambda child_id: child_id.address_type == 'Invoice')[:1]

            # self.partner_shipping_id = self.partner_id.search(
            #     [('parent_id', '=', self.partner_id.id),l
            #      ('address_type', '=', 'Shipping')], limit=1)

            self.partner_shipping_id = self.partner_id if self.partner_id.child_ids.filtered(
                lambda child_id: child_id.address_type == 'Shipping').ids == [] else self.partner_id.child_ids.filtered(
                lambda child_id: child_id.address_type == 'Shipping')[:1]

    def order_confirm(self):
        if self.warehouse_id:
            stock_move_line = []
            self.state = 'Confirmed'

            source_location_id = self.warehouse_id.stock_location_id.id
            destination_location_id = self.env['stock.location.ept'].search(
                            [('address_type', '=', 'Customer')], limit=1).id
            product_name = str(self.warehouse_id.name) + ' -> ' + str(self.env['stock.location.ept'].search([('address_type', '=', 'Customer')],limit=1).name)

            warehouses = [self.warehouse_id.id]
            for order_line in self.order_line_ids:
                if order_line.warehouse_id.id not in warehouses and order_line.warehouse_id.id != False:
                    warehouses.append(order_line.warehouse_id.id)

            for warehouse in warehouses:
                if warehouse == self.warehouse_id.id:
                    for order_line in self.order_line_ids.filtered(lambda child_id: child_id.warehouse_id.id == False or child_id.warehouse_id.id == self.warehouse_id.id):
                        order_line.state = 'Confirmed'
                        stock_move_line.append(
                            (0, 0, {
                                'name': order_line.product_id.name + ' : ' + product_name,
                                'product_id': order_line.product_id.id,
                                'uom_id': order_line.uom_id.id,
                                'source_location_id': source_location_id,
                                'destination_location_id': destination_location_id,
                                'qty_to_deliver': order_line.quantity,
                                'qty_done': 0,
                                'sale_line_id': order_line.id
                            })
                        )
                else:
                    for order_line in self.order_line_ids.filtered(lambda child_id: child_id.warehouse_id.id == warehouse):
                        order_line.state = 'Confirmed'
                        stock_move_line.append(
                            (0, 0, {
                                'name': order_line.product_id.name + ' : ' + product_name,
                                'product_id': order_line.product_id.id,
                                'uom_id': order_line.uom_id.id,
                                'source_location_id': order_line.warehouse_id.id,
                                'destination_location_id': destination_location_id,
                                'qty_to_deliver': order_line.quantity,
                                'qty_done': 0,
                                'sale_line_id': order_line.id
                            })
                        )

                stock_picking_id = self.env['stock.picking.ept'].create({
                    'partner_id': self.partner_id.id,
                    'sale_order_id': self.id,
                    'transaction_type': 'Out',
                    'move_ids': stock_move_line
                })
        else:
            raise ValidationError("Location Not Found")

    def compute_delivery_order_count(self):
        self.delivery_order_count = len(self.picking_ids)

    def action_view_delivery_order(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale_ept.action_stock_picking_out")

        if len(self.picking_ids) > 1:
            action['domain'] = [('id', 'in', self.picking_ids.ids)]
            # action['views'] = [(self.env.ref('sale_ept.view_stock_picking_tree').id, 'tree')]
        elif len(self.picking_ids) == 1:
            action['views'] = [(self.env.ref('sale_ept.view_stock_picking_form').id, 'form')]
            action['res_id'] = self.picking_ids.id

        return action

    def action_view_stock_move(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale_ept.action_stock_move")

        if len(self.order_line_ids.stock_move_ids) > 1:
            action['domain'] = [('id', 'in', self.order_line_ids.stock_move_ids.ids)]
            # action['views'] = [(self.env.ref('sale_ept.view_stock_move_tree').id, 'tree')]
        elif len(self.order_line_ids.stock_move_ids) == 1:
            action['views'] = [(self.env.ref('sale_ept.view_stock_move_form').id, 'form')]
            action['res_id'] = self.order_line_ids.stock_move_ids.id

        return action
