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

    salesperson_eval = fields.Boolean(
        string="Exclure de l'évaluation du vendeur",
        tracking=True,
    )

    salesperson_eval_reason = fields.Char(
        string='Raison',
        tracking=True
    )
