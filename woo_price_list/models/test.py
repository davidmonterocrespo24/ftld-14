import json

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

print(res)