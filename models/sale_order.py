# -*- coding: utf-8 -*-

from odoo import models, fields


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
        ], string='Invoice Payment Status', compute='_get_invoice_status', store=True, readonly=True)
    
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
    