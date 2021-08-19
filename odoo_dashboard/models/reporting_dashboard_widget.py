import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import ast

_logger = logging.getLogger(__name__)


class ReportingDashboardWidget(models.Model):
    _name = 'reporting.dashboard.widget'

    user_id = fields.Many2one(comodel_name='res.users', string='User', required=True)
    sql_query = fields.Text(string='SQL query')
    widget_type = fields.Selection(
        [
            ('WidgetSingleX', 'WidgetSingleX'),
            ('WidgetLastX', 'WidgetLastX'),
            ('WidgetXVsY', 'WidgetXVsY'),
        ],
        string='Widget type',
        default='WidgetLastX',
        required=True,
    )
    result = fields.Text(string='Result')
    column_name = fields.Text(string='Column name')
    dict_data = fields.Text(string='Dictionnary data')
    name = fields.Char(string='Widget name', required=True)
    sequence = fields.Integer(string='Sequence', default=0)
    is_enabled = fields.Boolean(string='Enabled', default=True)
    note = fields.Text(string='Note')
    result_format_help = fields.Text('Result format help')
    access_group_ids = fields.Many2many(
        comodel_name='reporting.access.group', string='Access groups'
    )
    database_connection_id = fields.Many2one(
        comodel_name='database.connection', string='Database connection', required=True
    )

    @api.onchange('widget_type')
    def onchange_widget_type(self):
        if self.widget_type == 'WidgetSingleX':
            self.result_format_help = (
                'Data retrieved from SQL request should follow this format:\n\r'
                + ' [{\'X_VALUE\':123}], \n\r'
                + 'Case is sensitive and column names are mandatory'
            )
        elif self.widget_type == 'WidgetLastX':
            self.result_format_help = (
                'Data retrieved from SQL request should follow this format:\n\r'
                + ' [{\'KEY_COL\':\'2021-01\','
                + ' \'TOTAL\':\'20000\'},{\'KEY_COL\':\'2021-02\','
                + ' \'TOTAL\':\'30000\'}], \n\r'
                + 'Case is sensitive and column names are mandatory'
            )
        elif self.widget_type == 'WidgetXVsY':
            self.result_format_help = (
                'Data retrieved from SQL request should follow this format:\n\r'
                + ' [{\'X_VALUE\':123, \'Y_VALUE\':4432,}], \n\r'
                + 'Case is sensitive and column names are mandatory'
            )

    @api.multi
    def has_access(self, user_id):
        for ag_id in self.access_group_ids:
            if ag_id.has_user(user_id):
                return True
        return False

    @api.multi
    def get_dict(self):
        dict_data = ast.literal_eval(self.dict_data)
        return dict_data

    @api.multi
    def process_data(self, columns, rows, data):
        if len(data) == 0:
            if self.widget_type == 'WidgetLastX':
                data = [{'KEY_COL': 'N/A', 'TOTAL': 0, 'CURRENCY': 'USD'}]
            elif self.widget_type == 'WidgetXVsY':
                data = [
                    {
                        'Y_VALUE': 0,
                        'CURRENCY': 'USD',
                        'CODE': 'N/A',
                        'NAME': 'N/A',
                        'X_VALUE': 0,
                    }
                ]
        self.result = str(data)
        self.column_name = str(columns)
        dict_data = {
            'id': self.id,
            'note': self.note,
            'widget_type': self.widget_type,
            'data': data,
            'write_date': self.write_date,
            'column_name': columns,
            'widget_name': self.name,
            'sequence': self.sequence,
        }
        self.dict_data = str(dict_data)

    @api.multi
    def action_request(self):
        columns, rows, data = self.database_connection_id.get_data(self.sql_query)
        self.process_data(columns, rows, data)

    @api.model
    def schedule_update_widget_action(self):
        widget_ids = self.env['reporting.dashboard.widget'].search(
            [('is_enabled', '=', True)]
        )
        for widget_id in widget_ids:
            widget_id.action_request()
