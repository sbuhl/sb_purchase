# -*- coding: utf-8 -*-

from odoo import _,models
from odoo.exceptions import UserError


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def write(self, vals):
        """ Override to handle the "inventory mode" and create the inventory move. """
        allowed_fields = self._get_inventory_fields_write()
        if self._is_inventory_mode() and any(field for field in allowed_fields if field in vals.keys()):
            if any(quant.location_id.usage == 'inventory' for quant in self):
                # Do nothing when user tries to modify manually a inventory loss
                return
            if any(field for field in vals.keys() if field not in allowed_fields):
                raise UserError(_("Quant's editing is restricted, you can't do this operation."))
            self = self.sudo()
        return super(StockQuant, self).write(vals)
