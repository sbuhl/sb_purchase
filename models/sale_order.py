# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = 'sale.order'

    # add tracking to this existing field
    referrer_id = fields.Many2one(tracking=True)

    sbu_field = fields.Boolean('TODO SBU FIELD')

    def write(self, values):
        res = super().write(values)

        if 'sbu_field' in values and not self._context.get('ignore_sbu_field'):
            orders, invoices = self.get_recursively_not_directly_related()
            orders.with_context(ignore_sbu_field=True).sbu_field = values['sbu_field']
            invoices.with_context(ignore_sbu_field=True).sbu_field = values['sbu_field']

        return res

    def get_recursively_not_directly_related(self, all_orders=None, all_invoices=None):
        # Care that it could auto discover one that has already been
        # discovered and enter infinite loop
        all_invoices = all_invoices or self.env['account.move']
        all_orders = all_orders or self.env['sale.order']
        all_orders |= self
        for order in self:
            related_invoices = order.order_line.invoice_lines.move_id
            related_orders = related_invoices.line_ids.sale_line_ids.order_id
            new_discovered_orders = related_orders.filtered(lambda o: o not in all_orders)
            oo, ii = new_discovered_orders.get_recursively_not_directly_related()
            all_invoices |= related_invoices | ii
            all_orders |= related_orders | oo
        return all_orders, all_invoices
