# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class Product(models.Model):

    _name = 'product.ept'
    _description = 'Product Demo'

    name = fields.Char(string="Product Name", help="Name of Product", required=True)
    sku = fields.Char(string="SKU", help="SKU of Product", required=True)
    weight = fields.Float(string="weight", help="weight of Product", digits=(6, 2))
    length = fields.Float(string="length", help="length of Product", digits=(6, 2))
    volume = fields.Float(string="Volume", help="Volume of Product", digits=(6, 2))
    width = fields.Float(string="Width", help="Width of Product", digits=(6, 2))
    barcode = fields.Char(string="Barcode", help="Barcode of Product")
    product_type = fields.Selection(selection=[('Storable', 'Storable'), ('Consumable', 'Consumable'), ('Service', 'Service')])
    sale_price = fields.Float(string="Sale Price", help="Sale Price of Product", digits=(6, 2), default=1.00)
    cost_price = fields.Float(string="Cost Price", help="Product Price of Product", digits=(6, 2), default=1.00)
    category_id = fields.Many2one(string="Category of Product", comodel_name='product.category.ept')
    uom_id = fields.Many2one(string="UOM", comodel_name='product.uom.ept')
    description = fields.Char(string="Description", help="Description of Product")
    product_stock = fields.Float(string="Product Stock", help="Product Stock",
                                 compute="compute_product_stock", store=False)
    tax_ids = fields.Many2many(string="Customer Taxes", help="Tax", comodel_name='account.tax.ept', domain=[('tax_use', '=', 'Sales')])

    def compute_product_stock(self):
        total_in = 0
        total_out = 0
        location_ids = []
        if self.env.context.get('location'):
            location_ids.append(self.env.context.get('location'))
        else:
            for location in self.env['stock.warehouse.ept'].search([]).stock_location_id:
                location_ids.append(location.id)

        for product in self:
            for move_in in self.env['stock.move.ept'].search([('product_id','=',product.id),('destination_location_id','in',location_ids)]):
                total_in += move_in.qty_done
            for move_out in self.env['stock.move.ept'].search([('product_id','=',product.id),('source_location_id','in',location_ids)]):
                total_out += move_out.qty_done

        self.product_stock = total_in - total_out

    def update_stock(self):
        # action = self.env['ir.actions.actions']._for_xml_id('sale_ept.action_product_stock_update')
        # return action

        action = {
            'name': _('Product Stock Action'),
            'view_mode': 'form',
            'res_model': 'product.stock.update.ept1',
            'view_id': self.env.ref('sale_ept.view_product_update_form').id,
            'type': 'ir.actions.act_window',
            'target': 'new'
        }
        return action
