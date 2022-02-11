# -*- coding: utf-8 -*-

from odoo import fields, models,api
from odoo.exceptions import ValidationError

class State(models.Model):

    _name = 'res.state.ept'
    _description = 'State Demo ex2'

    name = fields.Char(string="Name of State", help="State Name")
    code = fields.Char(string="Short Code of State", help="Short Code")
    country_id = fields.Many2one(string="Country", comodel_name='res.country.ept')
    city_ids = fields.One2many(string="States", comodel_name='res.city.ept', inverse_name='state_id')

    @api.constrains('code')
    def check_state_code(self):
        if self.search([('id','!=',self.id),('code','=',self.code)]):
            raise ValidationError("State Code All Ready Exists")

