# -*- coding: utf-8 -*-
{
    'name': "FLTDCA Custom",

    'summary': """
        FLTDCA Custom""",

    'description': """
        FLTDCA Custom
    """,

    'author': "rvcsdev",
    'website': "https://github.com/rvcsdev",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm', 'sale_crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'sql/restrict_mode_hash_table.sql',
        'data/cron_data.xml',
        'views/stock_picking_views.xml',
        #"'views/purchase_views.xml',
        'report/report_tracking_ref_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}