# -*- coding: utf-8 -*-
import dateutil.utils
from odoo import fields, models, api, _


class SalesPersonLeadCount(models.Model):
    _name = 'salesperson.lead.count'
    _description = 'Sales Person Lead'

    sales_person_name = fields.Many2one(string="Sales Person", comodel_name='res.users')
    count_num_pipeline = fields.Integer(string="Count Number of Pipelines", compute='compute_calculate_total'
                                        )
    total_revenue = fields.Float(string="Total Revenue", help="Total Revenue", compute='compute_calculate_total',
                                 )
    total_quotation = fields.Integer(string="Total Quotation", help="Total Quotation",
                                     compute='compute_calculate_total')
    total_sale_order = fields.Integer(string="Total Sale Order", help="Total Sale Order",
                                      compute='compute_calculate_total')
    sum_total_amount = fields.Float(string="Sum of total Amount", help="Sum Of Total Amount",
                                    compute='compute_calculate_total')
    percentage_revenue_to_order_amount = fields.Float(string="Percentage",
                                                      help="percentage of conversation amount from expected revenue to sales order total amount.",
                                                      compute='compute_calculate_total')
    partner_lead_id = fields.Many2one(string="Partner Lead Rel", comodel_name='partner.lead.rel.ept')
    lead_ids = fields.Many2many(string="Lead", comodel_name='crm.lead',
                                domain="['|',('partner_id','=',partner_id),('partner_id','=',partner_contact_ids)]")

    @api.depends('lead_ids')
    def compute_calculate_total(self):
        """
        compute count of pipeline as count of lead with sales person
        compute total_quotation as count of order that created base on lead but still not conformed
        compute total_revenue as total of sale order that created base on current selected partner's lead
        and make sure the invoice will generate from sale order
        compute total_sale_order as count of order that created base on lead and there invoice also be created
        compute percentage_revenue_to_order_amount calculate base on expected_revenue of lead and total_revenue
        :return:
        """
        for sale_person_line in self:
            sale_person_line.count_num_pipeline = len(sale_person_line.lead_ids)
            sale_person_line.total_quotation = len(
                self.env['sale.order'].search([('opportunity_id', 'in', sale_person_line.lead_ids.ids),
                                               ('state', '=', 'draft'),
                                               ('user_id', '=', sale_person_line.sales_person_name.id)]))
            sale_order_ids = self.env['sale.order'].search([('opportunity_id', 'in', sale_person_line.lead_ids.ids),
                                                            ('state', '=', 'sale'),
                                                            ('user_id', '=', sale_person_line.sales_person_name.id)])
            sale_person_line.total_revenue = sum(order.amount_total for order in sale_order_ids)
            sale_person_line.total_sale_order = len(sale_order_ids)
            sale_person_line.sum_total_amount = sum(line.price_subtotal for line in sale_order_ids.order_line)
            expected_revenue = sum(lead.expected_revenue for lead in sale_person_line.lead_ids)
            sale_person_line.percentage_revenue_to_order_amount = (sale_person_line.total_revenue * 100) / expected_revenue
