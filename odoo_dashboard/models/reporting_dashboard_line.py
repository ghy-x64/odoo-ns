import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import pyodbc
import ast

_logger = logging.getLogger(__name__)


class ReportingDashboardLine(models.Model):
    _name = 'reporting.dashboard.line'
    _order = 'sequence asc'

    sequence = fields.Integer(string='Sequence', default=0)
    widget_id = fields.Many2one(
        comodel_name='reporting.dashboard.widget', string='Widget', required=True
    )
    dashboard_id = fields.Many2one(
        comodel_name='reporting.dashboard', ondelete='cascade'
    )

    @api.multi
    def get_dict(self):
        dict_data = self.widget_id.get_dict()
        dict_data['line_id'] = self.id
        dict_data['sequence'] = self.sequence
        return dict_data
