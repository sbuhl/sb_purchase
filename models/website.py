# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.http import request


class Website(models.Model):
    _inherit = 'website'

    company_ids = fields.Many2many('res.company', string="Companies")

    def _get_warehouse_available(self):
        if request and request.session.get('GSE_FORCED_WAREHOUSE_ID'):
            gse_wh_id = int(request.session['GSE_FORCED_WAREHOUSE_ID'])
            if gse_wh_id in request.env['stock.warehouse'].sudo().search([('company_id', '=', self.company_id.id)]).ids:
                return gse_wh_id
            else:
                request.session.pop('GSE_FORCED_WAREHOUSE_ID')

        if request and request.session.get('GSE_FORCED_COMPANY_ID'):
            gse_company_id = int(request.session['GSE_FORCED_COMPANY_ID'])
            return self.env['stock.warehouse'].sudo().search([('company_id', '=', gse_company_id)], limit=1).id

        return super()._get_warehouse_available()

    def get_company_ids(self):
        import pudb;pu.db
        return self.env['res.company'].sudo().search([('website_ids', 'in', self.id)])
