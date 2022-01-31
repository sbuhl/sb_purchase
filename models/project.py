# -*- coding: utf-8 -*-

from odoo import fields, models


class Tasks(models.Model):
    _name = "project.task"
    _inherit = "project.task"

    
    purchase_order = fields.Many2one("purchase.order")
    purchase_requisition = fields.Many2one("purchase.requisition", string="Call For Tender")
