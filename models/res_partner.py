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

    @api.model
    def create(self, vals):
        self._handle_nif_vat_sync(vals)
        return super().create(vals)

    def write(self, values):
        self._handle_nif_vat_sync(values)
        return super().write(values)

    @api.model
    def _handle_nif_vat_sync(self, vals):
        if 'nif' in vals:
            vals['vat'] = vals['nif']
