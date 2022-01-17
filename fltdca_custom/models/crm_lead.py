# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
	_inherit = 'crm.lead'

	# sale_amount_total = fields.Monetary(compute='_compute_sale_amount_total', string="Sum of Orders", help="Untaxed Total of Confirmed Orders", currency_field='company_currency', store=True)
	# sale_number = fields.Integer(compute='_compute_sale_amount_total', string="Number of Quotations", store=True)

	quotation_no = fields.Integer(compute='_compute_sale_count', string='No. of Quotation', store=True)
	sale_no = fields.Integer(compute='_compute_sale_count', string='No. of Sale Order', store=True)
	invoice_no = fields.Integer(compute='_compute_sale_count', string='No. of Invoice Paid', store=True)

	@api.depends('order_ids', 'order_ids.state', 'order_ids.invoice_ids', 'order_ids.invoice_ids.state')
	def _compute_sale_count(self):
		for record in self:
			quotation_no = 0 
			sale_no = 0 
			invoice_no = 0 
			order_ids = self.env['sale.order'].search([('opportunity_id','=',record.id)])
			for order in order_ids:
				if order.state in ['draft','sent']:
					quotation_no += 1
				if order.state in ['sale', 'done']:
					sale_no += 1
				for invoice in order.invoice_ids:
					if invoice.state in ['in_payment','paid']:
						invoice_no += 1
			record.quotation_no = quotation_no
			record.sale_no = sale_no
			record.invoice_no = invoice_no