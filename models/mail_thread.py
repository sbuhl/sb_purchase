# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _get_mail_thread_data(self, request_list):
        res = super()._get_mail_thread_data(request_list)
        if self._name == "res.partner":
            res["hasWriteAccess"] = True
        return res

    def _message_create(self, values_list):
        if self._name == "res.partner":
            self = self.sudo()
        return super(MailThread, self)._message_create(values_list)
