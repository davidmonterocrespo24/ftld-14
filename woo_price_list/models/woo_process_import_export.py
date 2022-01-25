# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

import json
import logging


from odoo import api, models, fields, _


_logger = logging.getLogger("WooCommerce")


class WooProcessImportExport(models.TransientModel):
    _inherit = 'woo.process.import.export'
    _description = "WooCommerce Import/Export Process"

    woo_operation = fields.Selection(selection_add=[('expor_list_price', 'Export Price List')])


    def execute(self):
        if self.woo_operation == "expor_list_price":
            self.woo_export_expor_list_price()
        return super().execute()





    def woo_export_expor_list_price(self):
        json_final=[]
        pricelist=self.env["woo.instance.ept"].search([],limit=1).woo_pricelist_id
        name=""
        for r in pricelist.item_ids:
            if r.applied_on == '1_product':
                name=r.product_tmpl_id.product_variant_id.display_name+" "+str(r.min_quantity)
                woo_product_obj = self.env['woo.product.template.ept'].search([('product_tmpl_id', '=', r.product_tmpl_id.id)])
            elif r.applied_on == '0_product_variant':
                woo_product_obj = self.env['woo.product.product.ept'].search([('product_id', '=', r.product_id.id)])
                name=r.product_id.display_name+" "+str(r.min_quantity)
            if woo_product_obj.slug:
                data= """
                    {
                      "type": "package",
                      "filters": [
                           {
                                "qty": 1,
                                "type": "products",
                                "method": "in_list",
                                "value": [
                                     "producto-price-list"
                                ],
                                "product_exclude": {
                                     "on_wc_sale": "",
                                     "already_affected": "",
                                     "backorder": "",
                                     "values": []
                                }
                           }
                      ],
                      "title": "Producto price list",
                      "priority": "",
                      "enabled": "on",
                      "sortable_blocks_priority": [
                           "roles",
                           "bulk-adjustments"
                      ],
                      "additional": {
                           "conditions_relationship": "and",
                           "is_replaced": false,
                           "replace_name": "",
                           "is_replace_free_products_with_discount": false,
                           "free_products_replace_name": "",
                           "sortable_apply_mode": "consistently"
                      },
                      "conditions": [],
                      "cart_adjustments": [],
                      "limits": [],
                      "bulk_adjustments": {
                           "type": "bulk",
                           "qty_based": "not",
                           "discount_type": "price__fixed",
                           "ranges": [
                                {
                                     "from": 8,
                                     "to": "",
                                     "value": 500
                                }
                           ],
                           "table_message": ""
                      },
                      "role_discounts": [],
                      "get_products": {
                           "repeat": "-1",
                           "repeat_subtotal": ""
                      },
                      "options": {
                           "apply_to": "expensive",
                           "repeat": -1
                      },
                      "advertising": {
                           "discount_message": "",
                           "long_discount_message": "",
                           "sale_badge": ""
                      }
                 }
                    """

                res = json.loads(data)

                res['filters'][0]['value'][0]=woo_product_obj.slug
                res["title"]=name
                res["bulk_adjustments"]["ranges"][0]["from"]=r.min_quantity
                res["bulk_adjustments"]["ranges"][0]["value"]=r.fixed_price
                json_final.append(res)


        _logger.error(str(json_final))