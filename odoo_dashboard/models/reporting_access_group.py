import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import pyodbc
import ast

_logger = logging.getLogger(__name__)


class ReportingAccessGroup(models.Model):
    _name = 'reporting.access.group'

    name = fields.Char(string='Group', required=True)
    user_ids = fields.Many2many(comodel_name='res.users', string='User')

    @api.multi
    def has_user(self, user_id):
        for user in self.user_ids:
            if user.id == user_id:
                return True
        return False
