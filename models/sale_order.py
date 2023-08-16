# -*- coding: utf-8 -*-

from odoo import api, models, fields


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = 'sale.order'

    # add tracking to this existing field
    referrer_id = fields.Many2one(tracking=True)


