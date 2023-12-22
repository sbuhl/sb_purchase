# -*- coding: utf-8 -*-

from odoo import fields, models


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
    sales_per_year = fields.Float(string="Sales Yearly")
    COLOR_SELECTION = [
        ('#FF0000', 'Red'),    # HTML color code for red
        ('#00FF00', 'Green'),  # HTML color code for green
        ('#0000FF', 'Blue'),
    ]

    quality_check = fields.Selection(COLOR_SELECTION, widget='color',string="Quality Check")
