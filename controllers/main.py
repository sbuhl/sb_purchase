# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json

from odoo import http, SUPERUSER_ID
from odoo.http import request
from odoo.addons.mail.controllers import attachment, thread


class AttachmentController(attachment.AttachmentController):

    @http.route()
    def mail_attachment_upload(self, ufile, thread_id, thread_model, is_pending=False, **kwargs):
        if thread_model == 'res.partner':
            request.update_env(su=True)
        res = super().mail_attachment_upload(ufile, thread_id, thread_model, is_pending, **kwargs)

        vals = json.loads(res.response[0])
        try:
            token = request.env['ir.attachment']._generate_access_token()
            request.env['ir.attachment'].browse(vals['id']).access_token = token
            vals['accessToken'] = token
        except Exception:
            pass

        return request.make_json_response(vals)

    @http.route()
    def mail_attachment_delete(self, attachment_id, access_token=None):
        if request.env['ir.attachment'].browse(int(attachment_id)).sudo().create_uid == request.env.user:
            request.update_env(su=True)
            request.update_env(user=SUPERUSER_ID)
        return super().mail_attachment_delete(attachment_id, access_token)


class ThreadController(thread.ThreadController):
    @http.route()
    def mail_thread_messages(self, thread_model, thread_id, search_term=None, before=None, after=None, around=None, limit=30):
        if thread_model == 'res.partner':
            request.update_env(su=True)
        res = super().mail_thread_messages(thread_model, thread_id, search_term=search_term, before=before, after=after, around=around, limit=limit)

        for msg in res.get('messages'):
            for attach in msg.get('attachments', []):
                attach['accessToken'] = request.env['ir.attachment'].browse(attach['id']).access_token

        return res
