# -*- coding: utf-8 -*-
import dateutil.utils
from odoo import fields, models, api, _


class PartnerLead(models.Model):
    _name = 'partner.lead.rel.ept'
    _description = 'Partner Lead'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", help="Partner Name", index=True, default=lambda self: _('New'))
    from_date = fields.Date(string="From Date", help="From Date", default=fields.Date.today)
    to_date = fields.Date(string="To Date", help="To Date", default=fields.Date.today)
    partner_id = fields.Many2one(string="Partner", comodel_name='res.partner',
                                 domain="[('parent_id','=',False),('is_company','=',True)]")
    partner_contact_ids = fields.Many2many(string="Contact Partner", comodel_name='res.partner',
                                           domain="[('parent_id','=',partner_id)]")
    salesperson_lead_count_ids = fields.One2many(string="Sales Persons", comodel_name='salesperson.lead.count',
                                                 inverse_name="partner_lead_id")
    lead_ids = fields.Many2many(string="Lead", comodel_name='crm.lead',
                                domain="['|',('partner_id','=',partner_id),('partner_id','=',partner_contact_ids)]")
    total_revenue = fields.Float(string="Total Revenue", help="Total Revenue", compute='compute_total_revenue')
    count_pipeline = fields.Integer(string="Count Number of Pipelines", compute='compute_count_pipeline', store=False)
    count_sale_order = fields.Integer(string="Count Number of Sale Orders", compute='compute_count_pipeline',
                                      store=False)

    @api.model
    def create(self, vals):
        """
        to create a sequence for that partner lead model
        :param vals:
        :return: result as created sequence
        """
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('partner.lead.rel.ept') or _('New')
        result = super(PartnerLead, self).create(vals)
        return result

    @api.depends('lead_ids')
    def compute_count_pipeline(self):
        """
        compute count for count pipelines and sale order of selected partner
        :return:
        """
        for lead in self:
            lead.count_pipeline = len(self.env['crm.lead'].search(
                ['|', ('partner_id', '=', self.partner_id.id),
                 ('partner_id', '=', self.partner_contact_ids.id),
                 ('date_closed', '>=', self.from_date),
                 ('date_closed', '<=', self.to_date)
                 ]
            ))
            lead.count_sale_order = len(self.env['sale.order'].search(
                [('opportunity_id', 'in', self.lead_ids.ids),
                 ('invoice_ids.payment_state', 'in', ['paid', 'in_payment']),
                 ('date_order', '>=', self.from_date),
                 ('date_order', '<=', self.to_date),
                 ('picking_ids.state', '=', 'assigned')
                 ]
            ))

    @api.depends('lead_ids')
    def compute_total_revenue(self):
        """
        calculate total revenue from sale order that created from current lead
        :return:
        """
        self.total_revenue = 0
        if self.lead_ids:
            for partner_lead in self:
                leads = self.env['crm.lead'].search(
                    ['|', ('partner_id', '=', partner_lead.partner_id.id),
                     ('partner_id', '=', partner_lead.partner_contact_ids.id),
                     ('date_closed', '>=', partner_lead.from_date),
                     ('date_closed', '<=', partner_lead.to_date)
                     ])
                sale_order_ids = self.env['sale.order'].search([('opportunity_id', 'in', leads.ids),
                                                                ('state', '=', 'sale')])
                partner_lead.total_revenue = sum(order.amount_total for order in sale_order_ids)

    @api.onchange('partner_id', 'partner_contact_ids')
    def on_change_partner(self):
        if self.partner_id:
            self.partner_contact_ids = self.partner_id.child_ids
            if self.partner_contact_ids:
                self.lead_ids = self.env['crm.lead'].search(['|', ('partner_id', '=', self.partner_id.id),
                                                             ('partner_id', '=', self.partner_contact_ids.id)])
            else:
                self.lead_ids = self.env['crm.lead'].search([('partner_id', '=', self.partner_id.id)])

    def get_pipeline_details(self):
        """
        get the all lead with same sale person with selected lead and
        create the sale person line depend on that all lead
        :return:
        """
        sale_persons = self.lead_ids.user_id.ids
        salesperson_lead = []
        exists_salesperson = self.salesperson_lead_count_ids.sales_person_name.ids
        for sale_person in sale_persons:
            if sale_person not in exists_salesperson:
                lead_ids = self.lead_ids.filtered(lambda child_id: child_id.user_id.id == sale_person)
                salesperson_lead.append((0, 0, {'sales_person_name': sale_person,
                                                'lead_ids': lead_ids,
                                                'partner_lead_id': self.id}))
        self.salesperson_lead_count_ids = salesperson_lead

    def action_lead_view(self):
        """
        action to open the view form of crm lead base current lead partner
        :return: action
        """
        if not self.to_date:
            self.to_date = fields.Date.today()
        action = self.env["ir.actions.actions"]._for_xml_id("partner_lead_rel_ept.action_lead_view")
        action['domain'] = ['|', ('partner_id', '=', self.partner_id.id),
                            ('partner_id', '=', self.partner_contact_ids.id),
                            ('date_closed', '>=', self.from_date),
                            ('date_closed', '<=', self.to_date)
                            ]
        return action

    def action_partner_lead_view_sale_order(self):
        """
        action to open the tree view of sale order with base on current selected lead
        those are make invoice with full payments but not delivery order not validated
        :return:
        """
        action = self.env["ir.actions.actions"]._for_xml_id("partner_lead_rel_ept.action_partner_lead_view_sale_order")
        action['domain'] = [('opportunity_id', 'in', self.lead_ids.ids),
                            ('invoice_ids.payment_state', 'in', ['paid', 'in_payment']),
                            ('date_order', '>=', self.from_date),
                            ('date_order', '<=', self.to_date),
                            ('picking_ids.state', '=', 'assigned')
                            ]
        return action
