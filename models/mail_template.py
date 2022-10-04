# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    def generate_email(self, res_ids, fields):
        """ Based on l10n_ch implementation, adds attachments to the generated
        invoice.
        Those added attachments are the files from those custom fields:
        - bon_commande
        - bon_livraison
        """
        # result = {16: {'body_html': .., 'attachments': [..]}, 17: {...}}
        result = super().generate_email(res_ids, fields)
        if self.model != 'account.move':
            return result

        for record in self.env[self.model].browse(res_ids).filtered(lambda r: r.bon_commande or r.bon_livraison):
            inv_print_name = self._render_field('report_name', record.ids, compute_lang=True)[record.id]
            new_attachments = []

            if record.bon_commande:
                new_attachments.append(('bon_commande-' + inv_print_name + '.pdf', record.bon_commande))
            if record.bon_livraison:
                new_attachments.append(('bon_livraison-' + inv_print_name + '.pdf', record.bon_livraison))

            res = result[record.id]
            attachments_list = res.get('attachments', [])
            attachments_list.extend(new_attachments)
            res['attachments'] = attachments_list

        return result
