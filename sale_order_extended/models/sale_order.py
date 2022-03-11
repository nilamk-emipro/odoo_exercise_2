# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tests import Form


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    opportunity_new_id = fields.Many2one(comodel_name='crm.lead', string='Opportunity new')
    product_details = fields.Text(string='Details')
    is_all_picking_completed = fields.Boolean(string='Is Completed', help="Display all Data of all picking is done",
                                              store=False, compute="compute_all_picking_completed",
                                              search='_search_is_all_picking_completed')
    profit_value = fields.Float(string="Profit Value", help="Profit Value", compute='compute_calculate_profit')
    profit_percentage = fields.Float(string="Profit Percentage", help="Profit Percentage",
                                     compute='compute_calculate_profit')
    product_template_ids = fields.Many2many(comodel_name='product.template', string='Product')

    # # if self.order_line.product_id.filtered(lambda product_id: product_id.product_tmpl_id not in [self.product_template_ids._origin.ids]):
    # #     id = self.order_line.product_id.filtered(lambda product_id: product_id.product_tmpl_id not in [self.product_template_ids._origin.ids])
    # # product_ids = []
    # # self.order_line = ([(5, 0, 0)])
    # for variant_ids in self.product_template_ids._origin:
    #     if variant_ids.id not in self.order_line.product_id.product_tmpl_id.ids:
    #         for variant_id in self.env['product.product'].search(
    #                 [('product_tmpl_id', '=', variant_ids.id), ('qty_available', '>', 0)]):
    #             # product_ids.append(variant_id.id)
    #             self.order_line = ([(0, 0, {'product_id': variant_id.id})])
    # # line_ids = self.order_line.search([('product_id.product_tmpl_id.id', 'not in', self.product_template_ids._origin.ids)])
    # for line in self.order_line.filtered(
    #         lambda product: product.product_id.product_tmpl_id.id not in self.product_template_ids._origin.ids):
    #     # for lineid in line_ids.ids:
    #     self.order_line = ([(3, line.id, 0)])
    #
    # # self.order_line = [(6, 0, product_ids)]
    # for line in self.order_line:
    #     line.product_id_change()

    # def action_confirm(self):
    #     product_id = self.env.ref('sale_order_extended.product_new_product_1').id
    #
    #     # order_line_details = self.env['sale.order.line'].new({'product_id': product_id})
    #     # order_line_details.product_id_change()
    #     #
    #     # self.env['sale.order.line'].create({'order_id': self.id, 'product_id': product_id})
    #     #
    #     return super(SaleOrder, self).action_confirm()

    def add_deposit_product(self):
        for line in self.order_line.filtered(lambda child_id: child_id.product_id.deposit_product_id.id != False):
            if line.order_line_parent_id.id == False:
                self.env['sale.order.line'].create(
                    {'order_id': self.id,
                     'product_id': line.product_id.deposit_product_id.id,
                     'product_uom_qty': line.product_uom_qty * line.product_id.deposit_product_qty,
                     'order_line_child_id': line.id
                     })
            else:
                line.order_line_parent_id.product_uom_qty = line.product_uom_qty * line.product_id.deposit_product_qty

    def scan_product(self):
        action = {
            'name': _('Display Reserved product Details'),
            'view_mode': 'tree',
            'res_model': 'sale.order.line',
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref('sale_order_extended.sale_order_line_view_inherit').id,
            'target': 'new',
            'domain': [('product_id', 'in', self.order_line.product_id.ids),
                       ('id', 'not in', self.order_line.ids),
                       ('move_ids.state', '=', 'assigned')
                       ]
        }
        return action

    def confirm_and_validate(self):
        super(SaleOrder, self).action_confirm()
        self.picking_ids.button_validate()
        self.picking_ids.move_lines._set_quantities_to_reservation()
        self.picking_ids.with_context(skip_immediate=True).button_validate()

    @api.depends('picking_ids')
    def compute_all_picking_completed(self):
        if not self.picking_ids:
            self.is_all_picking_completed = False
        else:
            self.is_all_picking_completed = True
            if self.picking_ids.filtered(lambda picking_id: picking_id.state not in ['done', 'cancel']):
                self.is_all_picking_completed = False

    def _search_is_all_picking_completed(self, operator, value):
        query = """ SELECT sale_id FROM stock_picking
                            WHERE
                            sale_id not in (SELECT sale_id FROM stock_picking
                                    WHERE state not in ('done','cancel') and sale_id is not null)
                        """
        self.env.cr.execute(query)
        order_ids = self.env.cr.fetchall()
        return [('id', 'in', order_ids)]

    @api.depends('order_line')
    def compute_calculate_profit(self):
        self.profit_value = 0
        self.profit_percentage = 0
        if self.order_line:
            sale_price = sum(line.price_subtotal for line in self.order_line)
            cost_price = sum(line.order_line_cost_price for line in self.order_line)
            sale_price_of_product = sum(line.product_id.list_price * line.product_uom_qty for line in self.order_line)
            self.profit_value = sale_price - cost_price
            self.profit_percentage = self.profit_value * 100 / (sale_price_of_product - cost_price)

    @api.onchange('product_template_ids')
    def onchange_product_template_ids(self):
        for variant_ids in self.product_template_ids._origin:
            if variant_ids.id not in self.order_line.product_id.product_tmpl_id.ids:
                for variant_id in self.env['product.product'].search(
                        [('product_tmpl_id', '=', variant_ids.id), ('qty_available', '>', 0)]):
                    self.order_line = ([(0, 0, {'product_id': variant_id.id})])
        for line in self.order_line.filtered(
                lambda product: product.product_id.product_tmpl_id.id not in self.product_template_ids._origin.ids):
            self.order_line = ([(3, line.id, 0)])

        for line in self.order_line:
            line.product_id_change()

    @api.model
    def create(self, vals):
        return super(SaleOrder, self).create(vals)
