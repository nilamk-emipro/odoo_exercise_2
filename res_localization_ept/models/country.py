# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Country(models.Model):
    _name = 'res.country.ept'
    _description = 'Country Demo ex2'

    name = fields.Char(string="Name of Country", help="Country Name")
    code = fields.Char(string="Short Code of Country", help="Short Code")
    state_ids = fields.One2many(string="States", comodel_name='res.state.ept', inverse_name='country_id')

    _sql_constraints = [('unique_country_code', 'unique(code)', 'The Country Code must be unique')]

    # @api.model
    # def create(self, Vals):
    #     if Vals.get('code')== False:
    #         Vals.update({'code': '-'})
    #     new_recored = super(Country, self).create(Vals)
    #     return new_recored

    # def search(self, args, offset=0, limit=None, order=None, count=False):
    #     if len(args) > 0:
    #         # args.append(['code','ilike',args[0][2]])
    #         args=['|',('name', 'ilike', args[0][2]),('code','ilike',args[0][2])]
    #     return super(Country, self).search(args)

    # def write(self,vals):
    #     vals.update({'code':'IND'})
    #     return super(Country, self).write(vals)

    # def unlink(self):
    #     if self.code == 'IND':
    #         return super(Country, self).unlink()

    # def copy(self, default=None):
    #     default = {'name': self.name+'- copy'}
    #     return super(Country, self).copy(default)


    @api.model
    def name_get(self):
        data = []
        for country in self:
            display_data = country.name + ' - ' + country.code
            data.append((country.id, display_data))
        return data
