# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Odoo - NS Mobile Apps",
    'summary': """Odoo - NS Mobile Apps""",
    'description': """
        Odoo - NS Mobile App""",
    'author': 'GHY',
    'category': 'Apps',
    'version': '1.0',
    'depends': [
        'sale',
        'purchase',
    ],
    'data': [
        'views/purchase_order_view.xml',
        'views/sale_order_view.xml'
    ],
    'installable': True,
}
