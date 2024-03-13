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
    salesperson_eval = fields.Boolean(string="Exclure de l'évaluation du vendeur",tracking=True)
    salesperson_eval_reason = fields.Char(string='Raison', tracking=True)
    date_last_payment = fields.Date(compute='_compute_date_last_payment', store=True)
    exclude_from_review = fields.Boolean(string="Exclure de l'évaluation du vendeur", tracking=True, copy=False)

    def _compute_date_last_payment(self):
        last_payment_dates = {}        
        moves = self.filtered(lambda move: move.sudo().invoice_payments_widget)
        for move in moves:
            last_date = False
            invoice_payments_widget = move.sudo().invoice_payments_widget['content']
            for payment in invoice_payments_widget:
                if not last_date or payment['date'] > last_date:
                    last_date = payment['date']
            last_payment_dates[move.id] = last_date
        for move in moves:
            move.date_last_payment = last_payment_dates[move.id]

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if not self.env.user.has_group('account.group_account_manager'):
            raise UserError("La copie des facture a été désactivée.")
        return super().copy(default)

    def write(self, values):
        res = super().write(values)

        if 'exclude_from_review' in values and not self._context.get('ignore_exclude_from_review'):
            orders, invoices = self.line_ids.sale_line_ids.order_id.get_recursively_not_directly_related()
            orders.with_context(ignore_exclude_from_review=True).exclude_from_review = values['exclude_from_review']
            invoices.with_context(ignore_exclude_from_review=True).exclude_from_review = values['exclude_from_review']

        return res

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        for move in moves:
            orders, invoices = move.line_ids.sale_line_ids.order_id.get_recursively_not_directly_related()
            # get a random one, they should be syn'd anyway
            related_rec = orders and orders[0] or invoices and invoices[0] or None
            if related_rec:
                move.exclude_from_review = related_rec.exclude_from_review
        return moves


class AccountBankStatement(models.Model):
    _inherit = ['account.bank.statement', 'mail.activity.mixin']
    _name = 'account.bank.statement'
