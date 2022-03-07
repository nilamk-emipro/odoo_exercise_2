# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ProductStockUpdate(models.TransientModel):
    _name = 'merge.orders'
    _description = 'Merge Orders'

    merge_option = fields.Selection(
        selection=[('create_cancel', 'Create new order and cancel selected orders'),
                   ('create_delete', 'Create new order and delete selected orders'),
                   ('merge_cancel', 'Merge orders and cancel selected orders'),
                   ('merge_delete', 'Merge orders and delete selected orders')])

    merge_order_id = fields.Many2one(string="Select order for merge order", comodel_name='sale.order')

    @api.onchange('merge_option')
    def on_merge_option(self):
        """
        for get sale order id from context
        :return: selected sale order ids
        """
        if self.merge_option in ['merge_cancel', 'merge_delete']:
            return {'domain': {'merge_order_id': [('id', 'in', self.env.context.get('default_selected_ids'))]}}

    def create_order(self, selected_orders):
        """
        create new order from selected all order
        :param selected_orders: 
        :return: 
        """
        partner_details = self.env['sale.order'].new({'partner_id': selected_orders.partner_id.ids[0]})
        partner_details.onchange_partner_id()

        sale_order_id = self.env['sale.order'].create({
            'partner_id': selected_orders.partner_id.ids[0]
        })
        for sale_order_line in selected_orders.order_line:
            if self.env['sale.order.line'].search([('order_id', '=', sale_order_id.id),
                                                   ('product_id', '=', sale_order_line.product_id.id),
                                                   ('price_unit', '=', sale_order_line.price_unit),
                                                   ('tax_id', '=', sale_order_line.tax_id.ids)]):
                existing_order_line = self.env['sale.order.line'].search([('order_id', '=', sale_order_id.id),
                                                                          ('product_id', '=',
                                                                           sale_order_line.product_id.id),
                                                                          ('price_unit', '=',
                                                                           sale_order_line.price_unit),
                                                                          ('tax_id', '=', sale_order_line.tax_id.ids)])
                existing_order_line.product_uom_qty = existing_order_line.product_uom_qty + sale_order_line.product_uom_qty
            else:
                sale_order_line.copy(default={'order_id': sale_order_id.id})

    def cancel_all_order(self, selected_orders):
        """
        change the state of selected order which merge in new created order
        :param selected_orders: 
        :return: 
        """
        if self.merge_order_id:
            (selected_orders - self.merge_order_id).state = 'cancel'
        else:
            selected_orders.state = 'cancel'

    def merge_all_order(self, selected_orders):
        """
        Merge all selected order in one order which is selected in many2one merge_order_id
        :param selected_orders: 
        :return: 
        """
        sale_order_id = self.merge_order_id.id
        for sale_order_line in selected_orders.order_line:
            if self.env['sale.order.line'].search([('order_id', '=', sale_order_id),
                                                   ('product_id', '=', sale_order_line.product_id.id),
                                                   ('price_unit', '=', sale_order_line.price_unit),
                                                   ('tax_id', '=', sale_order_line.tax_id.ids)]):
                existing_order_line = self.env['sale.order.line'].search([('order_id', '=', sale_order_id),
                                                                          ('product_id', '=',
                                                                           sale_order_line.product_id.id),
                                                                          ('price_unit', '=',
                                                                           sale_order_line.price_unit),
                                                                          ('tax_id', '=', sale_order_line.tax_id.ids)])
                existing_order_line.product_uom_qty = existing_order_line.product_uom_qty + sale_order_line.product_uom_qty
            else:
                sale_order_line.copy(default={'order_id': sale_order_id.id})


    def delete_all_order(self, selected_orders):
        """
        delete the records which is selected and another record was from them
        :param selected_orders:
        :return:
        """
        if self.merge_order_id:
            (selected_orders - self.merge_order_id).unlink()
        else:
            selected_orders.unlink()

    def merge_order(self):
        if self.env['sale.order'].search(
                [('id', 'in', self.env.context.get('default_selected_ids')), ('state', '!=', 'draft')]):
            raise ValidationError("All Orders are having draft State")

        selected_orders = self.env['sale.order'].browse(self.env.context.get('default_selected_ids'))
        all_customer = all(order == selected_orders.partner_id.ids[0] for order in selected_orders.partner_id.ids)
        if all_customer == False:
            raise ValidationError("Only same customer order only can merge")

        if self.merge_option == 'create_cancel':
            self.create_order(selected_orders)
            self.cancel_all_order(selected_orders)

        if self.merge_option == 'create_delete':
            self.create_order(selected_orders)
            self.delete_all_order(selected_orders)

        if self.merge_option == 'merge_cancel':
            self.merge_all_order(selected_orders)
            self.cancel_all_order(selected_orders)

        if self.merge_option == 'merge_delete':
            self.merge_all_order(selected_orders)
            self.delete_all_order(selected_orders)
