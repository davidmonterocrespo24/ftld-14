# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
	_inherit = 'account.move'

	state = fields.Selection(selection_add=[('paid', 'Paid'),('open', 'Open')], ondelete={'paid': 'cascade','open': 'cascade'})