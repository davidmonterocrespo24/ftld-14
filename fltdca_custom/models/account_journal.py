# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class AccountJournal(models.Model):
	_inherit = 'account.journal'

	def check_restrict_mode_hash_table(self):
		journal_ids = self.search([
			('name', '=', 'Customer Invoices'),
			('restrict_mode_hash_table', '=', True),
		])
		for record in journal_ids:
			self._cr.execute('UPDATE account_journal SET restrict_mode_hash_table=false WHERE id in %s', [tuple([record.id])])
