{
    'name': 'Odoo iOS mobile dashboard',
    'version': '0.1',
    'category': 'tools',
    "website": "http://www.numberspeaks.com",
    'description': """
This module is required in order to use Odoo dashboard app (available only on Apple AppStore), 
it connects databases locally or remotely (MSSQL, MySQL, Postgres), schedules SQL requests and retrieve data. 
It could behave as a gateway between your database (Odoo ERP or not) and iOS devices (iPhone and iPad).
Published data have a mandatory format.
Widgets available:
- WidgetXVsY: Compare 2 numbers, widget will calculate difference and variation
- WidgetLastX: Could be used to display last x days, months, years data
- WidgetSingleX: Display a relevent number
User access can be managed through the menu access group.
Package pyodbc is required: apt-get install python3-pyodbc python-pyodbc
    """,
    'author': 'NS',
    "license": "LGPL-3",
    'depends': ['base'],
    'data': [
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
        'data/scheduler.xml',
        'views/reporting_dashboard_view.xml',
        'views/reporting_dashboard_widget_view.xml',
        'views/reporting_dashboard_line_view.xml',
        'views/database_connection_view.xml',
        'views/reporting_access_group_view.xml',
        'data/data.xml',
    ],
    'images': ['static/description/dashboard_screens.png'],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
