# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json
import logging
_logger = logging.getLogger(__name__)

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'


    def export_json(self):
        json_final=[]
        pricelist=self.env["woo.instance.ept"].search([],limit=1).woo_pricelist_id
        _logger.error(str(pricelist))

        for r in pricelist.item_ids:
            woo_product_obj = self.env['woo.product.product.ept'].search([('product_id', '=', r.product_tmpl_id.id)])
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
                res["title"]=r.product_tmpl_id.product_variant_id.display_name+" "+str(r.min_quantity)
                res["bulk_adjustments"]["ranges"][0]["from"]=r.min_quantity
                res["bulk_adjustments"]["ranges"][0]["value"]=r.fixed_price
                json_final.append(res)


        _logger.debug(str(json_final))

    
