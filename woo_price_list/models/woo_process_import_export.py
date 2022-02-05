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

    json_price_list = fields.Text(string="Json List Price", required=False, )


    def execute(self):
        if self.woo_operation == "expor_list_price":
            self.woo_export_expor_list_price()
            return {
                'name': _('WooCommerce Import/Export Process'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'woo.process.import.export',
                'target': 'new',
                'context': {'default_json_price_list': self.json_price_list,'default_woo_operation': "expor_list_price",'default_woo_instance_id': self.woo_instance_id.id}
            }






    def woo_export_expor_list_price(self):
        json_final=[]
        pricelist=self.env["woo.instance.ept"].search([],limit=1).woo_pricelist_id
        woo_products_ids= self.env['woo.product.template.ept'].search([])


        name=""
        sku=False
        for woo_p in woo_products_ids:
            item_ids=self.env['product.pricelist.item'].search([('product_tmpl_id','=',woo_p.product_tmpl_id.id)])
            data= """
                        {
                          "type": "package",
                          "filters": [
                               {
                                    "qty": 1,
                                    "type": "product_sku",
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


            # for r in pricelist.item_ids:
            #     sku=False
            #     if r.applied_on == '1_product':
            #         name=r.name+" "+str(r.min_quantity)+" "+str(r.price)
            #         woo_product_obj = self.env['woo.product.template.ept'].search([('product_tmpl_id', '=', r.product_tmpl_id.id)])
            #         sku= r.product_tmpl_id.default_code
            #     elif r.applied_on == '0_product_variant':
            #         woo_product_obj = self.env['woo.product.product.ept'].search([('product_id', '=', r.product_id.id)])
            #         name=r.product_id.display_name+" "+str(r.min_quantity)+ " "+str(r.price)
            #         sku= r.product_id.default_code
            #     if sku and woo_product_obj:


            res = json.loads(data)
            for i_id in item_ids:
                _logger.error(str(i_id.name))
                res["bulk_adjustments"]["ranges"].append({ 'from': i_id.min_quantity,'value': i_id.fixed_price})





            res['filters'][0]['value'][0]=woo_p.product_tmpl_id.default_code
            res["title"]=woo_p.display_name
            #res["bulk_adjustments"]["ranges"].extend(ranges)
            #res=json.dumps(res, indent=4, sort_keys=True)
            json_final.append(res)

        self.json_price_list=json_final
        _logger.error(str(json_final))