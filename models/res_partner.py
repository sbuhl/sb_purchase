# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = "res.partner"

    rccm = fields.Char(string='RCCM', help="Registre de Commerce et du Crédit Mobilier - CD/YYY/RCCM/xx-Y-xxxxx (where x = number and Y = capitalised letter)")
    id_nat = fields.Char(string='Id. Nat.', help="Identification Nationale - xx-Yxxxx-YxxxxxY (where x = number and Y = capitalised letter)")
    nif = fields.Char(string='NIF', help="Numéro d'Identification Fiscale - YxxxxxxxY (where x = number and Y = capitalised letter)")

    @api.constrains('rccm')
    def _check_rccm(self):
        pattern = r'^CD/[A-Z]{3}/RCCM/[0-9]{2}-[A-Z]{1}-[0-9]{5}$'
        for partner in self:
            if partner.rccm and not re.match(pattern, partner.rccm):
                raise ValidationError(_("RCCM number is not valid. It should respect the following: CD/YYY/RCCM/xx-Y-xxxxx (where x = number and Y = capitalised letter)"))

    @api.constrains('id_nat')
    def _check_id_nat(self):
        pattern = r'^[0-9]{2}-[A-Z]{1}[0-9]{4}-[A-Z]{1}[0-9]{5}[A-Z]{1}$'
        for partner in self:
            if partner.id_nat and not re.match(pattern, partner.id_nat):
                raise ValidationError(_("Id. Nat. number is not valid. It should respect the following: xx-Yxxxx-YxxxxxY (where x = number and Y = capitalised letter)"))

    @api.constrains('nif')
    def _check_nif(self):
        pattern = r'^[A-Z]{1}[0-9]{7}[A-Z]{1}$'
        for partner in self:
            if partner.nif and not re.match(pattern, partner.nif):
                raise ValidationError(_("NIF number is not valid. It should respect the following: YxxxxxxxY (where x = number and Y = capitalised letter)"))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._handle_nif_vat_sync(vals)
        return super(Partner, self).create(vals_list)

    def write(self, values):
        self._handle_nif_vat_sync(values)
        return super(Partner, self).write(values)

    @api.model
    def _handle_nif_vat_sync(self, vals):
        for partner in self: 
            if 'nif' in vals and partner.country_id.code == 'CD': 
                vals['vat'] = vals['nif'] if vals['nif'] else False
                
    @api.onchange('parent_id')
    def _onchange_parent_id(self):
        # Trigger the onchange event when the parent_id is changed
        # This will update the child fields based on the parent's values
        if self.parent_id:
            self.nif = self.parent_id.nif
            self.rccm = self.parent_id.rccm
            self.id_nat = self.parent_id.id_nat
            self.vat = self.parent_id.vat
        elif not self.parent_id:
            self.nif = False
            self.rccm = False
            self.id_nat = False
            self.vat = False

    @api.onchange('country_id')
    def _onchange_country_id(self): 
        self.nif = False
        self.rccm = False
        self.id_nat = False
        self.vat = False