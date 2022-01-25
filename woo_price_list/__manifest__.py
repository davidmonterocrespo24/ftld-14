# -*- coding: utf-8 -*-
{
    'name': "Price list woo",

    'summary': """
        Price list woo""",

    'description': """
        Price list woo
    """,

    'author': "Raul Rolando Jardinot Gonzalez",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','woo_commerce_ept'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        'views/lista_product_inherit.xml',

    ],

}