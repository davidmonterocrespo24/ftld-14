# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)

class AccountJournal(models.Model):
    _inherit = "account.journal"

    def action_open_reconcile(self):
        if self.type in ['bank', 'cash']:
            # Open reconciliation view for bank statements belonging to this journal
            lock_date = self.company_id._get_user_fiscal_lock_date() # defaults to date.min
            limit = int(self.env["ir.config_parameter"].sudo().get_param("account.reconcile.batch", 1000))
            bank_stmt = self.env['account.bank.statement.line'].search([
                ('statement_id.journal_id', 'in', self.ids),
                ('is_reconciled', '=', False),
                ('date', '>', lock_date),
                ('state', '=', 'posted'),
            ], limit=limit, order='date desc, id desc')
            return {
                'type': 'ir.actions.client',
                'tag': 'bank_statement_reconciliation_view',
                'context': {'statement_line_ids': bank_stmt.ids, 'company_ids': self.mapped('company_id').ids},
            }
        else:
            # Open reconciliation view for customers/suppliers
            action_context = {'show_mode_selector': False, 'company_ids': self.mapped('company_id').ids}
            if self.type == 'sale':
                action_context.update({'mode': 'customers'})
            elif self.type == 'purchase':
                action_context.update({'mode': 'suppliers'})
            return {
                'type': 'ir.actions.client',
                'tag': 'manual_reconciliation_view',
                'context': action_context,
            }