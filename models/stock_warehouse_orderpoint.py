# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.exceptions import UserError

class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    @api.returns('self', lambda value: value.id)
    def unlink(self, default=None):
        if not self.env.user.has_group('account.group_account_manager'):
            raise UserError("La suppression des orders move a été désactivée.")
        return super().delete(default)