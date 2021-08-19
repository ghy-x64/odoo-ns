import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import pyodbc
import ast

_logger = logging.getLogger(__name__)


class ReportingDashboard(models.Model):
    _name = 'reporting.dashboard'

    @api.multi
    def _compute_widget_count(self):
        for rec in self:
            rec.update({'widget_count': len(rec.widget_line_ids)})

    user_id = fields.Many2one(comodel_name='res.users', string='User', required=True)
    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence')
    is_default = fields.Boolean(string='Default', default=False)
    widget_line_ids = fields.One2many(
        comodel_name='reporting.dashboard.line',
        inverse_name='dashboard_id',
        string='line',
    )
    widget_count = fields.Integer(string='Widget count', compute=_compute_widget_count)

    @api.multi
    def add_widget(self, widget_id, sequence):
        for rec in self:
            line = self.env['reporting.dashboard.line'].create(
                {'dashboard_id': rec.id, 'widget_id': widget_id, 'sequence': sequence}
            )
            rec.update({'widget_line_ids': [(4, line.id)]})

    @api.multi
    def remove_widget(self, line_id):
        for rec in self:
            rec.update({'widget_line_ids': [(3, line_id)]})

    @api.multi
    def get_dict(self):
        dict_data = {
            'id': self.id,
            'name': self.name,
            'is_default': self.is_default,
            'sequence': self.sequence,
            'count': self.widget_count,
        }
        return dict_data
