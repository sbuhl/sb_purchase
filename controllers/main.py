# -*- coding: utf-8 -*-

from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request


class WebsiteSale(WebsiteSale):

    def _prepare_product_values(self, product, category, search, **kwargs):
        gse_forced_warehouse_id = int(request.params.pop('gse_forced_warehouse_id', 0))
        if gse_forced_warehouse_id and gse_forced_warehouse_id in request.env['stock.warehouse'].sudo().search([
            ('company_id', '=', request.website.company_id.id)]
        ).ids:
            request.session['GSE_FORCED_WAREHOUSE_ID'] = gse_forced_warehouse_id
            order = request.website.sale_get_order()
            if order and order.state == 'draft':
                order.warehouse_id = gse_forced_warehouse_id

                for line in order.order_line:
                    if line.exists():
                        order._cart_update(product_id=line.product_id.id, line_id=line.id, add_qty=0)

        return super()._prepare_product_values(product, category, search, **kwargs)

    @http.route('/website/company/force/<int:company_id>', type='http', auth='public', website=True, sitemap=False, multilang=False)
    def website_company_force(self, company_id, **kw):
        if company_id in request.website.get_company_ids().ids:
            request.session['GSE_FORCED_COMPANY_ID'] = company_id

        return request.redirect(request.httprequest.referrer)
