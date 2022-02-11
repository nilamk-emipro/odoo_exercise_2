# -*- coding: utf-8 -*-

from odoo import fields, models
from datetime import date
from odoo.exceptions import ValidationError

class CRMLead(models.Model):

    _name = 'crm.lead.ept'
    _description = 'CRM Lead Demo'

    # name = fields.Char(string="name", help="name")
    partner_id = fields.Many2one(string="Partner", comodel_name='res.partner.ept')
    order_ids = fields.One2many(string="Order", comodel_name='sale.order.ept', inverse_name='lead_id', readonly=True)
    team_id = fields.Many2one(string="Team", comodel_name='crm.team.ept')
    user_id = fields.Many2one(string="Sales Person", comodel_name='res.users', required=True)
    lead_line_ids = fields.One2many(string="Lead Lines", comodel_name='crm.lead.line.ept', inverse_name='lead_id')
    state = fields.Selection([
        ('New', 'New'),
        ('Qualified', 'Qualified'),
        ('Proposition', 'Proposition'),
        ('Won', 'Won'),
        ('Lost', 'Lost')
    ], string='State', default='New')
    won_date = fields.Date(string="Won Date", help="Won Date", readonly=True)
    lost_reason = fields.Char(string="Lost Reason", help="Reason of Lead Lost", readonly=True)
    next_followup_date = fields.Date(string="Next Followup Date", help="Next Followup Date")
    partner_name = fields.Char(string="Partner Name", help="Partner Name")
    partner_email = fields.Char(string="Email", help="Email")

    country_id = fields.Many2one(string="Country", comodel_name='res.country.ept')
    state_id = fields.Many2one(string="State", comodel_name='res.state.ept')
    city_id = fields.Many2one(string="City", comodel_name='res.city.ept')

    partner_phone_no = fields.Char(string="Phone No", help="Phone No")

    def state_qualified(self):
        self.state = 'Qualified'

    def state_proposition(self):
        self.state = 'Proposition'

    def state_won(self):
        self.state = 'Won'
        self.won_date = date.today()

    def state_lost(self):
        self.state = 'Lost'
        self.lost_reason['readonly'] = False

    def generate_sale_quotation(self):
        if self.partner_id:
            # shipping_id = self.partner_id.child_ids.filtered(
            #     lambda child_id: child_id.address_type == 'Shipping')[:1]
            # invoice_id = self.partner_id.child_ids.filtered(
            #     lambda child_id: child_id.address_type == 'Invoice')[:1]

            partner_details = self.env['sale.order.ept'].new({'partner_id': self.partner_id.id})
            partner_details.on_change_partner()

            sale_name = int(self.env['sale.order.ept'].search([])[-1].name.replace('SO00', '')) + 1
            sale_order_id = self.env['sale.order.ept'].create({
                'name': 'SO00' + str(sale_name),
                'partner_id': self.partner_id.id,
                'partner_invoice_id': partner_details.partner_invoice_id.id,
                'partner_shipping_id': partner_details.partner_shipping_id.id,
                'sale_order_date': date.today(),
                'sales_persons': self.user_id.id,
                'lead_id': self.id
            })
            for product_line in self.lead_line_ids:
                sale_order_line_id = self.env['sale.order.line.ept'].create(
                    {
                        'order_no_id': sale_order_id.id,
                        'product_id': product_line.product_id.id,
                        'name': product_line.name,
                        'quantity': product_line.expected_sell_qty,
                        'unit_price': product_line.product_id.sale_price,
                        'uom_id': product_line.uom_id.id
                    }
                )
        else:
            raise ValidationError("Add Partner Details First")

    def generate_customer(self):
        if self.partner_id.id == False:
            if self.partner_name != False:
                new_partner_id = self.env['res.partner.ept'].create({'name':self.partner_name,
                                                    'email':self.partner_email,
                                                    'phone':self.partner_phone_no,
                                                    'country':self.country_id.id,
                                                    'state':self.state_id.id,
                                                    'city':self.city_id.id
                                                    })
                self.partner_id = new_partner_id.id
            else:
                raise ValidationError("At Least Partner Name Must be enter")



