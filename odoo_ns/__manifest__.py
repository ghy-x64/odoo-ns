# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Odoo - NS Mobile Apps",
    'summary': """Approve SO PO from iOS device""",
    'description': """
        Approve SO PO from iOS device""",
    'author': 'Numberspeaks',
    "website": [
    	"http://www.numberspeaks.com/2020/10/12/odoo-so-po-mobile-approval/",
    	"https://github.com/ghy-x64/odoo-ns",
    ],
    'category': 'Apps',
    'version': '1.0',
    'license': "AGPL-3",
    'depends': [
        'sale',
        'purchase',
    ],
    'data': [
        'views/purchase_order_view.xml',
        'views/sale_order_view.xml'
    ],
    'images': [
    	'static/description/odoo-ns-odoo-store.png'
    ],
    'installable': True,
}
