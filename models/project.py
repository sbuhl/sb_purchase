# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Tasks(models.Model):
    _inherit = "project.task"

    sale_order = fields.Many2one("sale.order")
    direct_purchase = fields.Many2one("purchase.order", string="Ref Final Supplier")
    indirect_purchase = fields.Many2one("purchase.order", string="Ref Atimex")
    
    final_supplier = fields.Char(related="direct_purchase.partner_id.name", string="Final Supplier")
    dp_name = fields.Char(related="direct_purchase.name", string="PO Ref")
    dp_po_state = fields.Selection(related="direct_purchase.state", string="PO Status")
    dp_receipt_status = fields.Selection(related="direct_purchase.receipt_status", string="Reception Status")
    dp_date_approve = fields.Datetime(related="direct_purchase.date_approve", string="Confirmation Date")
    
    indirect_supplier = fields.Char(related="indirect_purchase.partner_id.name", string="Indirect Supplier")
    ip_name = fields.Char(related="indirect_purchase.name", string="PO Atimex")
    ip_po_state = fields.Selection(related="indirect_purchase.state", string="Atimex PO Status")
    ip_receipt_status = fields.Selection(related="indirect_purchase.receipt_status", string="Atimex Rec. Status")
    ip_date_approve = fields.Datetime(related="indirect_purchase.date_approve", string="Atimex Conf. Date")
    ip_date_scheduled = fields.Datetime(related="indirect_purchase.picking_ids.scheduled_date", string="Scheduled Date")
    ip_date_done = fields.Datetime(related="indirect_purchase.picking_ids.date_done", string="Effective Date")

    fd_location_dest = fields.Char(compute="_compute_final_location_dest", string="Destination")
    fd_scheduled_date = fields.Datetime(compute="_compute_final_dest_date", string="Final Dest. Scheduled Date")
    fd_forwarder = fields.Char(compute="_compute_final_forwarder", string="Forwarder")
    fd_forwarder_ref = fields.Char(compute="_compute_final_forwarder_ref", string="Forwarder Ref")
    
    @api.depends("indirect_purchase.name", "direct_purchase.picking_ids.location_dest_id", "indirect_purchase.picking_ids.location_dest_id")
    def _compute_final_location_dest(self):
        for record in self:
            if record.indirect_purchase.name:
                record.fd_location_dest = record.indirect_purchase.picking_ids.location_dest_id.warehouse_id.name
            else:
                record.fd_location_dest = record.direct_purchase.picking_ids.location_dest_id.warehouse_id.name
    
    @api.depends("indirect_purchase.name", "direct_purchase.picking_ids.scheduled_date", "indirect_purchase.picking_ids.scheduled_date")
    def _compute_final_dest_date(self):
        for record in self:
            if record.indirect_purchase.name:
                record.fd_scheduled_date = record.indirect_purchase.picking_ids.scheduled_date
            else:
                record.fd_scheduled_date = record.direct_purchase.picking_ids.scheduled_date
                
    @api.depends("indirect_purchase.name", "direct_purchase.picking_ids.carrier_id.name", "indirect_purchase.picking_ids.carrier_id.name")
    def _compute_final_forwarder(self):
        for record in self:
            if record.indirect_purchase.name:
                record.fd_forwarder = record.indirect_purchase.picking_ids.carrier_id.name
            else:
                record.fd_forwarder = record.direct_purchase.picking_ids.carrier_id.name

    @api.depends("indirect_purchase.name", "direct_purchase.picking_ids.carrier_tracking_ref", "indirect_purchase.picking_ids.carrier_tracking_ref")
    def _compute_final_forwarder_ref(self):
        for record in self:
            if record.indirect_purchase.name:
                record.fd_forwarder_ref = record.indirect_purchase.picking_ids.carrier_tracking_ref
            else:
                record.fd_forwarder_ref = record.direct_purchase.picking_ids.carrier_tracking_ref
    
    