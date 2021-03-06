# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

import json
import logging
import  requests

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
                'context': {'default_json_price_list': self.json_price_list,
                            'default_woo_operation': "expor_list_price",
                            'default_woo_instance_id': self.woo_instance_id.id}
            }

    def woo_export_expor_list_price(self):
        json_final = []
        pricelist = self.woo_instance_id.woo_pricelist_id
        woo_products_ids = self.env['woo.product.template.ept'].search([])

        name = ""
        sku = False
        for woo_p in woo_products_ids:
            if woo_p.product_tmpl_id.default_code:
                item_ids = self.env['product.pricelist.item'].search([('product_tmpl_id', '=', woo_p.product_tmpl_id.id)],
                                                                     order="min_quantity")
                if not item_ids:
                    continue
                data = """
                            {
                              "type": "single_item",
                              "rule_type": "common",
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
                f = 1
                for i_id in item_ids:
                    if i_id.min_quantity == 0 and i_id.fixed_price == 0:
                        continue
                    _logger.error(str(i_id.name))
                    res["bulk_adjustments"]["ranges"].append(
                        {'from': f, 'to': i_id.min_quantity, 'value': i_id.fixed_price})
                    f = i_id.min_quantity + 1

                res['filters'][0]['value'][0] = woo_p.product_tmpl_id.default_code
                res["title"] = woo_p.display_name
                # res["bulk_adjustments"]["ranges"].extend(ranges)
                # res=json.dumps(res, indent=4, sort_keys=True)
                json_final.append(res)
            else:
                for woo_pv_id in woo_p.woo_product_ids:
                    item_ids = self.env['product.pricelist.item'].search([('product_id', '=', woo_pv_id.product_id.id)],
                                                                         order="min_quantity")
                    if not item_ids:
                        continue
                    data = """
                            {
                              "type": "single_item",
                              "rule_type": "common",
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
                    res = json.loads(data)
                    f = 1
                    for i_id in item_ids:
                        if i_id.min_quantity == 0 and i_id.fixed_price == 0:
                            continue
                        _logger.error(str(i_id.name))
                        res["bulk_adjustments"]["ranges"].append(
                            {'from': f, 'to': i_id.min_quantity, 'value': i_id.fixed_price})
                        f = i_id.min_quantity + 1

                    res['filters'][0]['value'][0] = woo_pv_id.product_id.default_code
                    res["title"] = woo_pv_id.product_id.display_name
                    json_final.append(res)





        self.json_price_list = json.dumps(json_final, indent=4)
        _logger.error(str(json_final))
        self.send_to_wordpress( json.dumps(json_final, indent=4))



    def action_send_to_wordpress(self):
        self.send_to_wordpress(self.json_price_list)

    def send_to_wordpress(self,json_final):

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43', }
        wp_login = self.woo_instance_id.woo_host+'/wp-login.php'
        wp_admin = self.woo_instance_id.woo_host+'/wp-admin/admin.php?page=wdp_settings&tab=tools'
        datas={
            'log':self.woo_instance_id.woo_admin_username, 'pwd':self.woo_instance_id.woo_admin_password, 'wp-submit':'Log In',
            'redirect_to':wp_admin, 'testcookie':'1'
        }
        with requests.Session() as s:
            request=s.post(wp_login, headers=headers, data=datas)
            data_json={
                'wdp-import-data-reset-rules': 1,
                'wdp-import': '',
                'wdp-import-type': 'rules'   ,
                'wdp-import-data':json_final}
            _logger.error(data_json)
            json_resp=s.post(self.woo_instance_id.woo_host+'/wp-admin/admin.php?page=wdp_settings&tab=tools', headers=headers, data=data_json,verify=False)


