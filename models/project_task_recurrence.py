# -*- coding: utf-8 -*-

from odoo import api, models


class ProjectTaskRecurrence(models.Model):
    _name = "project.task.recurrence"
    _inherit = "project.task.recurrence"

    @api.model
    def _get_recurring_fields(self):
        return [
            "message_partner_ids",
            "company_id",
            "description",
            "displayed_image_id",
            "email_cc",
            "parent_id",
            "partner_email",
            "partner_id",
            "partner_phone",
            "planned_hours",
            "project_id",
            "display_project_id",
            "project_privacy_visibility",
            "sequence",
            "tag_ids",
            "recurrence_id",
            "name",
            "recurring_task",
            "analytic_account_id",
            "user_ids",
        ]
