# -*- coding: utf-8 -*-

from odoo import fields, models


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

    derniere_date_paiement = fields.Date(compute='_compute_derniere_date_paiement')

    def _compute_derniere_date_paiement(self):
        for move in self:
            last_date = False
            for payment in move.sudo()._get_reconciled_info_JSON_values():
                if not last_date or payment['date'] > last_date:
                    last_date = payment['date']
            move.derniere_date_paiement = last_date
