import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import pyodbc

_logger = logging.getLogger(__name__)


class DatabaseConnection(models.Model):
    _name = 'database.connection'

    name = fields.Char(string='Database connection name', required=True)
    server = fields.Char(string='Server')
    server_type = fields.Selection(
        [('pyodbc', 'PyODBC'), ('mysql', 'MySQL'), ('localhost', 'Localhost')],
        string='Server type',
    )
    username = fields.Char(string='Username')
    password = fields.Char(string='Password')
    database = fields.Char(string='Database')

    @api.multi
    def reformat_data(self, columns, rows):
        data = []
        for row in rows:
            if type(row) is pyodbc.Row:
                new_row = []
                for ele in row:
                    _logger.debug(type(ele))
                    if type(ele).__name__ in ['long', 'Decimal']:
                        ele = float(ele)
                    elif type(ele).__name__ == 'datetime':
                        ele = ele.strftime('%Y-%m-%d')
                    new_row.append(ele)
                data.append(dict(zip(columns, new_row)))
            elif type(row) is dict:
                new_dict = {}
                for key in row:
                    _logger.debug(type(row[key]))
                    if type(row[key]).__name__ in ['long', 'Decimal']:
                        new_dict[key.upper()] = float(row[key])
                if new_dict:
                    row = new_dict
                data.append(row)
        _logger.debug(rows)
        _logger.debug(columns)
        _logger.debug(data)
        return data

    @api.multi
    def get_data(self, sql_query):
        if self.server_type == 'pyodbc':
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:'
                + self.server
                + ';DATABASE='
                + self.database
                + ';UID='
                + self.username
                + ';PWD='
                + self.password
            )
            cursor = cnxn.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            columns = [column[0].upper() for column in cursor.description]
            data = self.reformat_data(columns, rows)
            return (columns, rows, data)
        elif self.server_type == 'mysql':
            raise UserError(_('MySQL is not implemented yet.'))
        elif self.server_type == 'localhost':
            self.env.cr.execute(sql_query)
            rows = self.env.cr.dictfetchall()
            columns = [key.upper() for key in rows[0]] if len(rows) > 0 else []
            data = self.reformat_data(columns, rows)
            return (columns, rows, data)
        else:
            raise UserError(_('Server type unknown %s: ' % self.server_type))
