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
    salesperson_eval = fields.Boolean(
        string="Exclure de l'évaluation du vendeur",
        tracking=True,
    )
    salesperson_eval_reason = fields.Char(
        string='Raison', tracking=True,
    )
    derniere_date_paiement = fields.Date(compute='_compute_derniere_date_paiement')

    sbu_field = fields.Boolean('TODO SBU FIELD')

    def _compute_derniere_date_paiement(self):
        for move in self:
            last_date = False
            for payment in move.sudo()._get_reconciled_info_JSON_values():
                if not last_date or payment['date'] > last_date:
                    last_date = payment['date']
            move.derniere_date_paiement = last_date

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if not self.env.user.has_group('account.group_account_manager'):
            raise UserError("La copie des facture a été désactivée.")
        return super().copy(default)

    def write(self, values):
        res = super().write(values)

        if 'sbu_field' in values and not self._context.get('ignore_sbu_field'):
            orders, invoices = self.line_ids.sale_line_ids.order_id.get_recursively_not_directly_related()
            orders.with_context(ignore_sbu_field=True).sbu_field = values['sbu_field']
            invoices.with_context(ignore_sbu_field=True).sbu_field = values['sbu_field']

        return res


class AccountBankStatement(models.Model):
    _inherit = ['account.bank.statement', 'mail.activity.mixin']
    _name = 'account.bank.statement'
