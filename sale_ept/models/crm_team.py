# -*- coding: utf-8 -*-

from odoo import fields, models

class CRMTeam(models.Model):

    _name = 'crm.team.ept'
    _description = 'CRM Team Demo'

    name = fields.Char(string="CRM Team Name", help="Name of CRM Team")
    team_leader_id = fields.Many2one(string="Team Leader", comodel_name='res.users')