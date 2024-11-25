# -*- coding: utf-8 -*-
import logging

from odoo import api, models, fields, SUPERUSER_ID


_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    last_sale_date = fields.Date(string="Last Sale Date")

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
    ], string='Invoice Payment Status', compute='_get_invoice_payment_status')

    @api.depends('state', 'order_line.invoice_lines.move_id.payment_state')
    def _get_invoice_payment_status(self):
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
                order.invoice_payment_status = 'not_paid'
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

    exclude_from_review = fields.Boolean(string="Exclude from the salesperon's evaluation", tracking=True, copy=False)

    def write(self, values):
        res = super().write(values)
        if 'exclude_from_review' in values and not self._context.get('ignore_exclude_from_review'):
            orders, invoices = self.get_recursively_not_directly_related()
            orders.with_context(ignore_exclude_from_review=True).exclude_from_review = values['exclude_from_review']
            invoices.with_context(ignore_exclude_from_review=True).exclude_from_review = values['exclude_from_review']
        return res

    def get_recursively_not_directly_related(self, all_orders=None, all_invoices=None, visited_orders=None):
        # Initialisation des ensembles pour stocker les commandes et factures traitées
        all_invoices = all_invoices or self.env['account.move']
        all_orders = all_orders or self.env['sale.order']
        # La variable visited_orders est nécessaire pour éviter la récursion infinie et optimiser le traitement.
        # Utiliser un set pour visited_orders assure que les opérations de vérification sont rapides (O(1)).
        visited_orders = visited_orders or set()
        # Ajoutez les commandes actuelles à l'ensemble des commandes traitées
        all_orders |= self
    
        # Parcourez chaque commande
        for order in self:
            # Si la commande a déjà été visitée, sautez-la pour éviter la récursion infinie
            if order.id in visited_orders:
                continue
            # Marquez la commande actuelle comme visitée
            visited_orders.add(order.id)
            # Récupérez les factures liées à la commande
            related_invoices = order.order_line.invoice_lines.move_id
            # Récupérez les commandes liées aux factures découvertes
            related_orders = related_invoices.line_ids.sale_line_ids.order_id
            # Filtrez les nouvelles commandes non encore explorées
            new_discovered_orders = related_orders.filtered(lambda o: o not in all_orders)
            # Récursion avec les nouvelles commandes découvertes
            oo, ii = new_discovered_orders.get_recursively_not_directly_related(all_orders, all_invoices, visited_orders)
            # Ajoutez les nouvelles factures et commandes aux ensembles
            all_invoices |= related_invoices | ii
            all_orders |= related_orders | oo
        return all_orders, all_invoices

    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        today_date = fields.Date.today()
        for line in self.order_line:
            if not line.product_id.last_sale_date:
                line.product_id.sudo().write({'last_sale_date': today_date})
        return result

    def update_last_sale_date(self):
        sale_orders = self.env['sale.order'].search(
            [('state', '=', 'sale'),
             ('date_order', '>=', '2022-01-01'),
             ('date_order', '<=', '2024-05-31')],
            order='date_order desc'
        )
        _logger.info(f"Found {len(sale_orders)} confirmed sale orders.")
        processed_products = set()

        for sale_order in sale_orders:
            sale_date = sale_order.date_order.date()
            _logger.info(f"Processing sale order {sale_order.name} with date {sale_date}")
            for line in sale_order.order_line:
                product = line.product_id
                if product.id not in processed_products:
                    if not product.last_sale_date or product.last_sale_date < sale_date:
                        _logger.info(f"Updating last_sale_date for product: {product.name} to {sale_date}")
                        product.write({'last_sale_date': sale_date})
                        processed_products.add(product.id)
        return True  # Retourne une valeur pour indiquer que l'action a été complétée
