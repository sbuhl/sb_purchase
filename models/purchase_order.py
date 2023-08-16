# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"

    is_international = fields.Boolean()

    def button_approve(self):
        self._add_supplier_to_product()
        res = super(PurchaseOrder, self).button_approve()
        return res


class PurchaseOrderLine(models.Model):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"

    quantity_available_gse = fields.Float(related="product_id.qty_available")
