from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute


class WebsiteSaleInherit(WebsiteSale):

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        brand_list = request.httprequest.args.getlist('brands')
        brand_values = [int(v) for v in brand_list if v]
        brand_set = {v for v in brand_values}

        res = super(WebsiteSaleInherit, self).shop(page=0, category=None, search='', min_price=0.0, max_price=0.0,
                                                   ppg=False, **post)
        if brand_list:
            product_search = request.env['product.template'].search([('id', 'in', res.qcontext['products'].ids),
                                                                     ('product_brand_ept_id', 'in', brand_values)])
            total = len(res.qcontext['products'])
        else:
            product_search = res.qcontext['products']
            total = res.qcontext['search_count']
        pager = request.website.pager(url="/shop", total=total, page=page, step=res.qcontext['ppg'], scope=7, url_args=post)

        res.qcontext.update({'product_brand': request.env['product.brand.ept'].search([]),
                             'brand_set': brand_set,
                             'bins': TableCompute().process(product_search),
                             'products': product_search,
                             'search_count': total,
                             'pager': pager
                             })
        return res
