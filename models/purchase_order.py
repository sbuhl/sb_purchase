# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"

    is_international = fields.Boolean()

    def button_approve(self):
        self._add_supplier_to_product()
        res = super(PurchaseOrder, self).button_approve()
        return res

    invoice_payment_status = fields.Selection([
          ('no', 'Nothing to Pay'),
          ('not_paid', 'Not Paid'),
          ('in_payment', 'In Payment'),
          ('paid', 'Paid'),
          ('partially_paid', 'Partially Paid'),
      ], string='Invoice Payment Status', compute='_get_invoice_payment_status')

    @api.depends('state', 'order_line.invoice_lines.move_id.payment_state')
    def _get_invoice_payment_status(self):
        for order in self:
            related_invoices = order.order_line.invoice_lines.move_id
            if not related_invoices:  # If there are no invoices
                order.invoice_payment_status = 'no'
            else:
                if order.state not in ('sale', 'done'):
                    order.invoice_payment_status = 'no'
                elif all(invoice.payment_state == 'not_paid' for invoice in related_invoices):
                    order.invoice_payment_status = 'not_paid'
                elif any(invoice.payment_state == 'in_payment' for invoice in related_invoices):
                    order.invoice_payment_status = 'in_payment'
                elif all(invoice.payment_state == 'paid' for invoice in related_invoices):
                    order.invoice_payment_status = 'paid'
                elif any(invoice.payment_state == 'partial' for invoice in related_invoices):
                    order.invoice_payment_status = 'partially_paid'
                elif any(invoice.payment_state == 'paid' for invoice in related_invoices) and any(invoice.payment_state == 'not_paid' for invoice in related_invoices):
                    order.invoice_payment_status = 'partially_paid'
                else:
                    order.invoice_payment_status = 'no'

class PurchaseOrderLine(models.Model):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"

    quantity_available_gse = fields.Float(related="product_id.qty_available")
