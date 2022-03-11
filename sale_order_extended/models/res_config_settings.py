# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_sale_payment_term = fields.Boolean("Payment Term",
                                             implied_group='sale_order_extended.group_sale_payment_term',
                                             help="Allows to display payment terms based on rules")
    module_employee_ept = fields.Boolean("Employee")

    # sale_id = fields.Many2one('sale.order', string='Sale Order')
    # sale_payment_term_id = fields.Integer(related='sale_id.payment_term_id', string="Payment Term", readonly=False)

    # default_payment_term_id = fields.Selection([
    #     ('1', 'Immediate Payment'),
    #     ('7', '	End of Following Month')
    # ], 'Payment Term',
    #     default='1',
    #     default_model='sale.order')

    def set_values(self):
        super(ResConfigSettings, self).set_values()

