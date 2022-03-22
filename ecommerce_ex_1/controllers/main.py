from odoo import http
from odoo.http import request


class ProductDisplay(http.Controller):

    @http.route(['''/custom_page'''], type='http', website=True, auth='public')
    def product(self):
        return request.render("ecommerce_ex_1.custom_page", {})

    @http.route(['/product_page'], type='json', auth="public", website=True, csrf=False)
    def product_on_button_click(self, **kw):
        all_product = request.env['product.template'].sudo().search([('website_published', '=', True)], limit=1)
        return request.env['ir.ui.view']._render_template("ecommerce_ex_1.product_page",
                                                                  {'products': all_product})

