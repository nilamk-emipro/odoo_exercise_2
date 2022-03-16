# -*- coding: utf-8 -*-
from odoo import api, models

class DeliveryOrderReport(models.AbstractModel):
    _name = 'report.sale_ept.report_delivery_order_ept'
    _description = 'Delivery Order Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        stock_move_line = self.env['stock.move.ept'].search([('picking_id', 'in', self.env['stock.picking.ept'].browse(docids).ids)])
        products = self.env['product.ept'].browse(stock_move_line.product_id.ids)
        for stock_move in stock_move_line:
            docs.append({
                'product': stock_move.product_id.id,
                'picking': stock_move.picking_id.name,
                'quantity': stock_move.qty_done
            })

        return {
            'doc_ids': docids,
            'doc_model': 'mrp.bom',
            'docs': docs,
            'products': products
        }


class DeliveryOrderLocationReport(models.AbstractModel):
    _name = 'report.sale_ept.report_delivery_order_location_ept'
    _description = 'Delivery Order Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        stock_move_line = self.env['stock.move.ept'].search([('picking_id', 'in', self.env['stock.picking.ept'].browse(docids).ids)])
        products = self.env['product.ept'].browse(stock_move_line.product_id.ids)
        locations = self.env['stock.location.ept'].browse(stock_move_line.source_location_id.ids)
        for stock_move in stock_move_line:
            docs.append({
                'product': stock_move.product_id.id,
                'picking': stock_move.picking_id.name,
                'quantity': stock_move.qty_done,
                'location': stock_move.source_location_id.id
            })

        return {
            'doc_ids': docids,
            'doc_model': 'mrp.bom',
            'docs': docs,
            'products': products,
            'locations': locations
        }

