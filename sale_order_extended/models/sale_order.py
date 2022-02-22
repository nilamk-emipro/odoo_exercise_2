# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tests import Form

class SaleOrder(models.Model):
    _inherit = ['sale.order']

    opportunity_new_id = fields.Many2one(comodel_name='crm.lead', string='Opportunity new')
    product_details = fields.Text(string='Details')

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
        # name = self.order_line.product_id.name
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

    def action_confirm(self):
        super(SaleOrder, self).action_confirm()

        # res_dict = self.picking_ids.button_validate()
        # Form(self.env[res_dict['res_model']].with_context(res_dict['context'])).save().process()

        self.picking_ids.button_validate()
        self.picking_ids.move_lines._set_quantities_to_reservation()
        self.picking_ids.with_context(skip_immediate=True).button_validate()








