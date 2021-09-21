# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    income_analytic_tag_ids = fields.Many2one(comodel_name='account.analytic.tag', string='Analytic Tags',company_dependent=True)
    expense_analytic_tag_ids = fields.Many2one(comodel_name='account.analytic.tag',  string='Analytic Tags',company_dependent=True)

    def _get_product_analytic_tags(self):
        self.ensure_one()
        return {
            'income': self.income_analytic_tag_ids or
                      self.categ_id.income_analytic_tag_ids,
            'expense': self.expense_analytic_tag_ids or
                       self.categ_id.expense_analytic_tag_ids
        }

class ProductCategory(models.Model):
    _inherit = 'product.category'

    income_analytic_tag_ids = fields.Many2one(comodel_name='account.analytic.tag', relation='income_analytic_tag_category_rel',string='Analytic Tags',company_dependent=True)
    expense_analytic_tag_ids = fields.Many2one(comodel_name='account.analytic.tag',relation= 'expense_analytic_tag_category_rel', string='Analytic Tags',company_dependent=True)