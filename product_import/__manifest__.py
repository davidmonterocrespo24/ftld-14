# -*- coding: utf-8 -*-

{
    'name': 'Product Image from URL',
    'summary': 'Product Images from Web URL and Path',
    'version': '14.0.1.0.0',
    'description': """Product Images from Web URL, Product Images from path, local""",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'category': 'Sales',
    'license': 'AGPL-3',
    'images': ['static/description/banner.png'],
    'depends': ['sale_management', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_url.xml',
        'wizard/product_import.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
