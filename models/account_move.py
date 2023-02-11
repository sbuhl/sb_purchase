# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = 'account.move'

    bon_commande = fields.Binary()

    bon_livraison = fields.Binary()

    paiement_filename = fields.Binary()

    date_rappel_manuel = fields.Date()

    preuve_paiement = fields.Boolean()

    dossier_complet = fields.Boolean()

    travaux_termines = fields.Boolean()

    salesperson_eval = fields.Boolean()

    salesperson_eval_reason = fields.Char(
        string='Raison',
    )

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if not self.env.user.has_group('account.group_account_manager'):
            raise UserError("La copie des facture a été désactivée.")
        return super().copy(default)
