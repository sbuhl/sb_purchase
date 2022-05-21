# -*- coding: utf-8 -*-

from odoo import fields, models


class Lead(models.Model):
    _name = 'crm.lead'
    _inherit = 'crm.lead'

    station = fields.Selection([("goma", "Goma"), ("bukavu", "Bukavu"), ("kinshasa", "Kinshasa"), ("kalemie", "Kalemie"), ("lubumbashi", "Lubumbashi"), ("bunia", "Bunia"), ("kigali", "Kigali"), ("kampala", "Kampala")], default="goma")  # noqa: E501
