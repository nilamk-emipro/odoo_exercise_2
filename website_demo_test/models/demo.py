# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class WebsiteDemo(models.Model):

    _name = 'demo.ept'
    _description = 'Website Demo'

    name = fields.Char(string="Website Name")
