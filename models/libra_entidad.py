# -*- coding: utf-8 -*-
import odoo
from odoo import tools, models, fields, api, _
from ast import literal_eval
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.http import request
import uuid
from odoo import http

class LibraEntidad(models.Model):
	_name = 'libra.entidad'

	name = fields.Char('Entidad')
	street = fields.Char('Calle')
	street2 = fields.Char('Calle')
	city = fields.Char('Ciudad')
	state_id = fields.Many2one('res.country.state', 'Estado')
	zip = fields.Char('C.P.')
	country_id = fields.Many2one('res.country', 'Pais')
	phone = fields.Char('Teléfono')
	fax = fields.Char('Fax')
	email = fields.Char('Correo electrónico')
	company_id = fields.Many2one('res.company', 'Empresa', default=lambda self: self.env['res.company']._company_default_get('libra.entidad'))
	users_ids = fields.Many2many('res.users', 'financiera_entidad_users_rel', 'user_id', 'entidad_id', string='Usuarios')
	journal_disponibles_ids = fields.Many2many('account.journal', 'financiera_disponibles_entidad_journal_rel', 'entidad_id', 'journal_id', string='Diarios')
	type = fields.Selection([('sucursal', 'Sucursal')], string='Tipo', default='sucursal')
	state = fields.Selection([('draft', 'Borrador'), ('confirm', 'Confirmado')], string='Estado', readonly=True, default='draft')
	journal_invoice_electronic_id = fields.Many2one('account.journal', 'Diario de factura electronica', domain="[('type', '=', 'sale')]")
	journal_invoice_id = fields.Many2one('account.journal', 'Diario de factura interna', domain="[('type', '=', 'sale')]")
	# Productos
	product_interes_id = fields.Many2one('product.product', 'Producto intereses ganados')
	product_punitorio_id = fields.Many2one('product.product', 'Producto punitorio ganados')
	product_seguro_id = fields.Many2one('product.product', 'Producto seguro ganados')
	product_ajuste_id = fields.Many2one('product.product', 'Producto otros conceptos ganados')
	product_refinanciacion_id = fields.Many2one('product.product', 'Producto refinanciacion ganadas')
	# Incobrable
	# journal_incobrable_id = fields.Many2one('account.journal', 'Diario de asientos incobrables')
	# account_capital_incobrable_id = fields.Many2one('account.account', 'Cuenta para registrar capital incobrable')
	# account_facturado_incobrable_id = fields.Many2one('account.account', 'Cuenta para registrar facturacion devengada como incobrable')

	@api.model
	def default_get(self, fields):
		rec = super(LibraEntidad, self).default_get(fields)
		context = dict(self._context or {})
		current_uid = context.get('uid')
		rec.update({
				'users_ids': [current_uid],
			})
		return rec

class ExtendsAccountJournal(models.Model):
	_name = 'account.journal'
	_inherit = 'account.journal'

	entidad_disponibles_ids = fields.Many2many('libra.entidad', 'financiera_disponibles_entidad_journal_rel', 'journal_id', 'entidad_id', string='Entidades')
	users_ids = fields.Many2many('res.users', 'user_journal_rel', 'user_id', 'journal_id', string='Usuarios disponibles')

class ExtendsCompany(models.Model):
	_inherit = 'res.company'
	_name = 'res.company'

	portal_url = fields.Char('Portal URL', help="Sin http.")
	template_registro_id = fields.Many2one('mail.template', 'Template registro de usuario')
	template_reseteo_id = fields.Many2one('mail.template', 'Template reseteo contrasena de usuario')
	server_email_id = fields.Many2one('ir.mail_server', 'Email de envio por defecto')