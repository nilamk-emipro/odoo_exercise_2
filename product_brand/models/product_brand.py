# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ProductBrand(models.Model):
    _inherit = ['website.published.multi.mixin']
    _name = 'product.brand.ept'

    name = fields.Char(string="Name", help="Name of Product Brand", required=True)
    website_id = fields.Many2one(comodel_name='website', string="Website")
    product_ids = fields.Many2many(comodel_name='product.template', inverse_name='product_brand_ept_id', string="Product")
    logo = fields.Binary(string="Logo", help="Logo")

    # def _get_search_domain(self, search, category, attrib_values, search_in_description=True):
    #     domains = super(ProductBrand, self)._get_search_domain(search, category, attrib_values, search_in_description)
    #     if attrib_values:
    #         ids = []
    #         for value in attrib_values:
    #             if value[0] == 0:
    #                 ids.append(value[1])
    #         if ids:
    #             domains.append(('product_brand_ept_id', 'in', ids))
    #
    #     return domains