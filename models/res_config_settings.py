# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    website_company_ids = fields.Many2many(related='website_id.company_ids', string='Website Companies', readonly=False)
