# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

# class SaleOrder(models.Model):
#     _inherit = "sale.order"

#     def _create_delivery_line(self, carrier, price_unit):
#         return False

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    manual_add = fields.Boolean(default=False, string='Manually Added')

    # Override to remove reset of price unit
    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        # price_unit = self._origin.price_unit
        # manual_add = self._origin.manual_add
        # if price_unit and price_unit > 0:
        #     self.price_unit = price_unit
        #     return
        # return super(SaleOrderLine, self).product_uom_change()
        # return True