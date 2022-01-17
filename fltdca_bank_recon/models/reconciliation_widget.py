# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)

class AccountReconciliation(models.AbstractModel):
    _inherit = "account.reconciliation.widget"

#     @api.model
#     def get_move_lines_for_bank_statement_line(self, st_line_id, partner_id=None, excluded_ids=None, search_str=False, offset=0, limit=None, mode=None):
#         """ Returns move lines for the bank statement reconciliation widget,
#             formatted as a list of dicts

#             :param st_line_id: ids of the statement lines
#             :param partner_id: optional partner id to select only the moves
#                 line corresponding to the partner
#             :param excluded_ids: optional move lines ids excluded from the
#                 result
#             :param search_str: optional search (can be the amout, display_name,
#                 partner name, move line name)
#             :param offset: offset of the search result (to display pager)
#             :param limit: number of the result to search
#             :param mode: 'rp' for receivable/payable or 'other'
#         """
#         statement_line = self.env['account.bank.statement.line'].browse(st_line_id)

#         if search_str:
#             domain = self._get_search_domain(search_str=search_str)
#         else:
#             domain = []

#         if partner_id:
#             domain.append(('partner_id', '=', partner_id))

#         if excluded_ids:
#             domain.append(('id', 'not in', tuple(excluded_ids)))

#         if mode == 'rp':
#             query, params = self._get_query_reconciliation_widget_customer_vendor_matching_lines(statement_line, domain=domain)
#         else:
#             query, params = self._get_query_reconciliation_widget_miscellaneous_matching_lines(statement_line, domain=domain)

#         trailing_query, trailing_params = self._get_trailing_query(statement_line, limit=limit, offset=offset)

#         self._cr.execute(query + trailing_query, params + trailing_params)
#         results = self._cr.dictfetchall()
#         if results:
#             recs_count = results[0].get('full_count', 0)
#         else:
#             recs_count = 0
#         move_lines = self.env['account.move.line'].browse(res['id'] for res in results).sorted(key=lambda r: r.date_maturity, reverse=True)

#         js_vals_list = []
#         for line in move_lines:
#             js_vals_list.append(self._prepare_js_reconciliation_widget_move_line(statement_line, line, recs_count=recs_count))
#         return js_vals_list
    
#     @api.model
#     def get_bank_statement_line_data(self, st_line_ids, excluded_ids=None):
#         """ Returns the data required to display a reconciliation widget, for
#             each statement line in self

#             :param st_line_id: ids of the statement lines
#             :param excluded_ids: optional move lines ids excluded from the
#                 result
#         """
#         results = {
#             'lines': [],
#             'value_min': 0,
#             'value_max': 0,
#             'reconciled_aml_ids': [],
#         }

#         if not st_line_ids:
#             return results

#         excluded_ids = excluded_ids or []

#         # Make a search to preserve the table's order.
#         bank_statement_lines = self.env['account.bank.statement.line'].search([('id', 'in', st_line_ids)])
#         results['value_max'] = len(bank_statement_lines)
#         reconcile_model = self.env['account.reconcile.model'].search([('rule_type', '!=', 'writeoff_button')])

#         # Search for missing partners when opening the reconciliation widget.
#         partner_map = self._get_bank_statement_line_partners(bank_statement_lines)

#         matching_amls = reconcile_model._apply_rules(bank_statement_lines, excluded_ids=excluded_ids, partner_map=partner_map)

#         # Iterate on st_lines to keep the same order in the results list.
#         bank_statements_left = self.env['account.bank.statement']
#         for line in bank_statement_lines:
#             if matching_amls[line.id].get('status') == 'reconciled':
#                 reconciled_move_lines = matching_amls[line.id].get('reconciled_lines')
#                 results['value_min'] += 1
#                 results['reconciled_aml_ids'] += reconciled_move_lines and reconciled_move_lines.ids or []
#             else:
#                 aml_ids = matching_amls[line.id]['aml_ids']
#                 bank_statements_left += line.statement_id

#                 amls = aml_ids and self.env['account.move.line'].browse(aml_ids).sorted(key=lambda r: r.date_maturity, reverse=True)
#                 line_vals = {
#                     'st_line': self._get_statement_line(line),
#                     'reconciliation_proposition': [self._prepare_js_reconciliation_widget_move_line(line, aml) for aml in amls],
#                     'model_id': matching_amls[line.id].get('model') and matching_amls[line.id]['model'].id,
#                 }

#                 # Add partner info if necessary
#                 line_partner = matching_amls[line.id].get('partner')

#                 if not line_partner and partner_map.get(line.id):
#                     line_partner = self.env['res.partner'].browse(partner_map[line.id])

#                 if line_partner:
#                     line_vals.update({
#                         'partner_id': line_partner.id,
#                         'partner_name': line_partner.name,
#                     })

#                 # Add writeoff info if necessary
#                 if matching_amls[line.id].get('status') == 'write_off':
#                     line_vals['write_off_vals'] = matching_amls[line.id]['write_off_vals']
#                     self._complete_write_off_vals_for_widget(line_vals['write_off_vals'])

#                 results['lines'].append(line_vals)

#         return results
    
    @api.model
    def _get_query_select_clause(self):
        return '''
            account_move_line.id,
            account_move_line.balance,
            account_move_line.amount_currency,
            account_move_line.date_maturity,
            account_move_line.currency_id,
            account_move_line.date
        '''
    
    @api.model
    def _get_trailing_query(self, statement_line, limit=None, offset=None):
        liquidity_lines, suspense_lines, other_lines = statement_line._seek_for_lines()

        if liquidity_lines.currency_id != liquidity_lines.company_currency_id:
            amount_matching_order_by_clause = '''
                account_move_line.balance = %s OR (
                    account_move_line.currency_id IS NOT NULL
                    AND
                    account_move_line.amount_currency = %s
                )
            '''
            params = [liquidity_lines.balance, liquidity_lines.amount_currency]
        else:
            amount_matching_order_by_clause = '''account_move_line.balance = %s'''
            params = [liquidity_lines.balance]

        trailing_query = '''
            ORDER BY
                account_move_line.date_maturity DESC,
                ''' + amount_matching_order_by_clause + ''' DESC
                
        '''
        if limit:
            trailing_query += ' LIMIT %s'
            params.append(limit)
        if offset:
            trailing_query += ' OFFSET %s'
            params.append(offset)
        return trailing_query, params
    
