# -*- coding: utf-8 -*-

from odoo import fields, models


class PurchaseOrder(models.Model):
    _name = "purchase.order"
    inherit = "purchase.order"

    is_international = fields.Boolean()
