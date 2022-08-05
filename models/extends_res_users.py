# -*- coding: utf-8 -*-
import odoo
from odoo import tools, models, fields, _, api

class ExtendsResUsers(models.Model):
	_name = 'res.users'
	_inherit = 'res.users'

	entidad_login_id = fields.Many2one('libra.entidad', "Entidad")
	entidad_ids = fields.Many2many('libra.entidad', 'financiera_entidad_users_rel', 'entidad_id', 'user_id', string='Entidades')
	journal_ids = fields.Many2many('account.journal', 'user_journal_rel', 'journal_id', 'user_id', string='Diarios disponibles')


	def __init__(self, pool, cr):
		""" Override of __init__ to add access rights on entidad_login_id
			Access rights are disabled by default, but allowed
			on some specific fields defined in self.SELF_{READ/WRITE}ABLE_FIELDS.
		"""
		init_res = super(ExtendsResUsers, self).__init__(pool, cr)
		# duplicate list to avoid modifying the original reference
		type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
		type(self).SELF_WRITEABLE_FIELDS.extend(['entidad_login_id'])
		# duplicate list to avoid modifying the original reference
		type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
		type(self).SELF_READABLE_FIELDS.extend(['entidad_login_id'])
		return init_res
	
	# update journal_ids if entidad_login_id changes
	@api.onchange('entidad_login_id')
	def _onchange_entidad_login_id(self):
		journal_ids = [g.id for g in self.entidad_login_id.journal_disponibles_ids]
		if self.entidad_login_id:
			self.journal_ids = [(6, 0, journal_ids)]
