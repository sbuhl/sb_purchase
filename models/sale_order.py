# -*- coding: utf-8 -*-

from odoo import api, models, fields


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = 'sale.order'

    # add tracking to this existing field
    referrer_id = fields.Many2one(tracking=True)

    invoice_payment_status = fields.Selection([
        ('no', 'Nothing to Pay'),
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
    ], string='Invoice Payment Status', compute='_get_invoice_payement_status', store=True, readonly=True)

    @api.depends('state', 'order_line.invoice_lines.move_id.payment_state')
    def _get_invoice_payement_status(self):
        """
        Compute the invoice payments status of a SO. Possible statuses:
        - nothing to pay: if the SO is not in status 'sale', or 'done', nothing is invoiced,
            so nothing has to be paid. This is also the default value if the conditions of
            no other status is met.
        - not_paid: if one invoiced has been created but not yet paid.
        - in_payment: if at least one invoice is in status 'in_payment'
        - paid: if all invoices are in status 'paid'
        - partial: if all invoices are in status 'partial'
        """
        for order in self:
            related_invoices = order.order_line.invoice_lines.move_id
            if not related_invoices:  # If there are no invoices
                order.invoice_payment_status = 'no_paid'
            else:
                if order.state not in ('sale', 'done'):
                    order.invoice_payment_status = 'no'
                elif any(invoice.payment_state == 'not_paid' for invoice in related_invoices):
                    order.invoice_payment_status = 'not_paid'
                elif any(invoice.payment_state == 'in_payment' for invoice in related_invoices):
                    order.invoice_payment_status = 'in_payment'
                elif all(invoice.payment_state == 'paid' for invoice in related_invoices):
                    order.invoice_payment_status = 'paid'
                elif any(invoice.payment_state == 'partial' for invoice in related_invoices):
                    order.invoice_payment_status = 'partially_paid'
                else:
                    order.invoice_payment_status = 'no'

