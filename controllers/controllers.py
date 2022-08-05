# -*- coding: utf-8 -*-
# from odoo import http


# class LibraBase(http.Controller):
#     @http.route('/libra_base/libra_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/libra_base/libra_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('libra_base.listing', {
#             'root': '/libra_base/libra_base',
#             'objects': http.request.env['libra_base.libra_base'].search([]),
#         })

#     @http.route('/libra_base/libra_base/objects/<model("libra_base.libra_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('libra_base.object', {
#             'object': obj
#         })
