# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models
from odoo.http import request


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _add_dispatch_parameters(cls, func):
        super()._add_dispatch_parameters(func)

        if request.session.get('GSE_FORCED_COMPANY_ID'):
            gse_company_id = int(request.session['GSE_FORCED_COMPANY_ID'])
            if gse_company_id in request.website.get_company_ids().ids:
                if gse_company_id not in request.context['allowed_company_ids']:
                    request.context['allowed_company_ids'].append(gse_company_id)
