# -*- coding: utf-8 -*-

from odoo import api, fields, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_new_quotation(self):
        action = super(CrmLead, self).action_new_quotation()
        action['context']['default_opportunity_new_id'] = self.id
        action['context']['default_tag_ids'].append((4, [self.env.ref('sale_order_extended.crm_lead_tag_new').id],0))
        return action
