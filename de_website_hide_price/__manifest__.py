# -*- coding: utf-8 -*-
{
    'name': "Website Hide Price",

    'summary': """
        Show/Hide Product Price""",

    'description': """
        Show/Hide product prices at website
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    'category': 'Website',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base','crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        #'views/templates.xml',
        #'data/website_hide_price.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}