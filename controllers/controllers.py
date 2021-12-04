# -*- coding: utf-8 -*-
# from odoo import http


# class SbPurchase(http.Controller):
#     @http.route('/sb_purchase/sb_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sb_purchase/sb_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sb_purchase.listing', {
#             'root': '/sb_purchase/sb_purchase',
#             'objects': http.request.env['sb_purchase.sb_purchase'].search([]),
#         })

#     @http.route('/sb_purchase/sb_purchase/objects/<model("sb_purchase.sb_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sb_purchase.object', {
#             'object': obj
#         })
