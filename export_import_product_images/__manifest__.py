# -*- coding: utf-8 -*-


{
    'name': 'Export or Import Product Images',
    'version': '1.0',
    'category': 'Sales Management',
    'sequence': 20,
    'summary': 'To Export o Import selected product images to a specified directory',
    'description': """
Export selected product images to a specified directory
==================================

This application allows you to Export selected product images to a specified directory.
    """,
    'author': 'credativ software (India) pvt ltd',
    'depends': ['product'],
    'data': [
        'wizard/export_product_images_view.xml',
'wizard/import_product_images_view.xml',
 "security/ir.model.access.csv",
    ],
    'demo': [],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
