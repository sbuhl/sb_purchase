# -*- coding: utf-8 -*-

from odoo import fields, models


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    rccm = fields.Char(string='NRC/RCCM')
    nif = fields.Char(string='NIF')
