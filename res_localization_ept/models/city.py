# -*- coding: utf-8 -*-

from odoo import fields, models

class City(models.Model):

    _name = 'res.city.ept'
    _description = 'City Demo ex2'

    name = fields.Char(string="Name of City", help="City Name")
    state_id = fields.Many2one(comodel_name='res.state.ept')

