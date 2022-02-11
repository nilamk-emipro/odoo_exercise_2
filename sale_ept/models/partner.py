# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Partner(models.Model):

    _name = 'res.partner.ept'
    _description = 'Partner Demo'

    name = fields.Char(string="Partner Name", help="Name of partner")
    street1 = fields.Char(string="street1", help="Street 1")
    street2 = fields.Char(string="street2", help="Street 2")

    country = fields.Many2one(string="Country", comodel_name='res.country.ept')
    state = fields.Many2one(string="State", comodel_name='res.state.ept')
    city = fields.Many2one(string="City", comodel_name='res.city.ept')

    zipcode = fields.Char(string="Zip Code", help="Zip Code")
    email = fields.Char(string="Email Address", help="Email Address")
    mobile = fields.Char(string="Mobile Number", help="Mobile Number")
    phone = fields.Char(string="Phone No", help="Phone No")
    image = fields.Image(string="Image", help="Image")
    website = fields.Char(string="Web site", help="WebSite")
    active = fields.Boolean(string="Active", default=True)

    parent_id = fields.Many2one(string="Partner", comodel_name='res.partner.ept')
    child_ids = fields.One2many(string="Child", comodel_name='res.partner.ept', inverse_name='parent_id')
    address_type = fields.Selection(
        selection=[('Invoice', 'Invoice'), ('Shipping', 'Shipping'), ('Contact', 'Contact')])


    def create_country(self):
        # self.env['res.country.ept'].create({'name':'Australia','code':''})
        # country = self.env['res.country.ept'].search([('name', 'ilike', 'Australia')])
        # # self.country.copy({'name': self.country.name +'- copy'})
        # # print(country)
        # country.unlink()
        country = self.env['res.country.ept']
        countries=country.browse([1,2,3,4,5,6,7,8])
        print(countries)



