# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, SUPERUSER_ID
from odoo.http import request
from odoo.addons.mail.controllers import discuss


class Website(discuss.DiscussController):

    @http.route()
    def mail_attachment_upload(self, ufile, thread_id, thread_model, is_pending=False, **kwargs):
        if thread_model == 'res.partner':
            request.update_env(user=SUPERUSER_ID)
        return super().mail_attachment_upload(ufile, thread_id, thread_model, is_pending, **kwargs)