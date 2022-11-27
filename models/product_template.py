# -*- coding: utf-8 -*-

from odoo import models
from odoo.http import request


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False, parent_combination=False, only_template=False):
        combination_info = super()._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist,
            parent_combination=parent_combination, only_template=only_template)

        if combination_info['product_id']:
            product = self.env['product.product'].sudo().browse(combination_info['product_id'])
            website = self.env['website'].get_current_website()
            website_company_id = request and request.session.get('GSE_FORCED_COMPANY_ID') or website.company_id.id
            combination_info.update({
                'gse_website_companies': [{
                    'id': company.id,
                    'name': company.name,
                    'address': company.partner_id.with_context(html_format=True, show_address_only=True).name_get()[0][1],  # contact_address_complete,
                    'selected': website_company_id == company.id,
                } for company in website.get_company_ids()],
                'gse_warehouses_qty_custo': [{
                    'id': wh.id,
                    'name': wh.name,
                    'address': wh.partner_id.with_context(html_format=True, show_address_only=True).name_get()[0][1],
                    'free_qty': product.with_context(warehouse=wh.id).free_qty,
                    'selected': website._get_warehouse_available() == wh.id,
                } for wh in self.env['stock.warehouse'].sudo().search([('company_id', '=', website_company_id)])],
            })
        else:
            combination_info.update({
                'gse_warehouses_qty_custo': [],
                'gse_website_companies': [],
            })

        return combination_info
