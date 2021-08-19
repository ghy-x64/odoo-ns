import openerp.http as http
from openerp import SUPERUSER_ID
from openerp import _
from openerp.http import request
from datetime import datetime, date, timedelta
import logging
import json

_logger = logging.getLogger(__name__)
import pytz


class MainController(http.Controller):
    @http.route(
        ['/lgf_reporting_app/data'], type='json', methods=['POST', 'GET'], auth="user"
    )
    def widget_request(self, **kwargs):
        values = dict(kwargs)
        widget_ids = request.env['reporting.dashboard.widget'].search(
            [('user_id', '=', request.uid), ('is_enabled', '=', True)], order='sequence'
        )
        data = []
        for widget in widget_ids:
            data.append(widget.get_dict())
        return json.dumps(data)

    @http.route(
        ['/lgf_reporting_app/list/widget'],
        type='json',
        methods=['POST', 'GET'],
        auth="user",
    )
    def list_widget_request(self, **kwargs):
        values = dict(kwargs)
        ag_ids = request.env['reporting.access.group'].search(
            [('user_ids', '=', request.uid)]
        )
        widget_ids = request.env['reporting.dashboard.widget'].search(
            [
                '&',
                '|',
                ('user_id', '=', request.uid),
                ('access_group_ids', 'in', ag_ids.ids),
                ('is_enabled', '=', True),
            ],
            order='sequence',
        )
        data = []
        for widget in widget_ids:
            data.append(widget.get_dict())
        return json.dumps(data)

    @http.route(
        ['/lgf_reporting_app/dashboard/<string:id>/list/widget_to_add'],
        type='json',
        methods=['POST', 'GET'],
        auth="user",
    )
    def list_widget_to_add_request(self, **kwargs):
        values = dict(kwargs)
        ag_ids = request.env['reporting.access.group'].search(
            [('user_ids', '=', request.uid)]
        )
        dashboard_id = request.env['reporting.dashboard'].browse([int(values['id'])])
        already_added_widget_ids = []
        for line in dashboard_id.widget_line_ids:
            already_added_widget_ids.append(line.widget_id.id)
        widget_ids = request.env['reporting.dashboard.widget'].search(
            [
                '&',
                '&',
                '|',
                ('user_id', '=', request.uid),
                ('access_group_ids', 'in', ag_ids.ids),
                ('is_enabled', '=', True),
                ('id', 'not in', already_added_widget_ids),
            ],
            order='sequence',
        )
        data = []
        for widget in widget_ids:
            data.append(widget.get_dict())
        return json.dumps(data)

    @http.route(
        ['/lgf_reporting_app/list/dashboard'],
        type='json',
        methods=['POST', 'GET'],
        auth="user",
    )
    def list_dashboard_request(self, **kwargs):
        values = dict(kwargs)
        dashboard_ids = request.env['reporting.dashboard'].search(
            [('user_id', '=', request.uid)], order='sequence'
        )
        data = []
        for dashboard in dashboard_ids:
            data.append(dashboard.get_dict())
        return json.dumps(data)

    @http.route(
        ['/lgf_reporting_app/add/dashboard/<string:name>/<string:sequence>'],
        type='json',
        methods=['POST', 'GET'],
        auth="user",
    )
    def add_dashboard_request(self, **kwargs):
        values = dict(kwargs)
        dashboard_id = request.env['reporting.dashboard'].create(
            {
                'name': values['name'],
                'user_id': request.uid,
                'sequence': int(values['sequence']),
            }
        )
        data = []
        data.append(dashboard_id.get_dict())
        return json.dumps(data)

    @http.route(
        ['/lgf_reporting_app/edit/dashboard/<string:id>/<string:name>'],
        type='json',
        methods=['POST', 'GET'],
        auth="user",
    )
    def edit_dashboard_request(self, **kwargs):
        values = dict(kwargs)
        dashboard_id = request.env['reporting.dashboard'].search(
            [('id', '=', int(values['id']))]
        )
        dashboard_id.name = values['name']
        data = []
        data.append(dashboard_id.get_dict())
        return json.dumps(data)

    @http.route(
        ['/lgf_reporting_app/remove/dashboard/<string:id>'],
        type='json',
        methods=['POST', 'GET'],
        auth="user",
    )
    def remove_dashboard_request(self, **kwargs):
        values = dict(kwargs)
        dashboard_id = request.env['reporting.dashboard'].search(
            [('id', '=', int(values['id']))]
        )
        dashboard_id.unlink()
        return json.dumps([True])

    @http.route(
        ['/lgf_reporting_app/dashboard/<string:id>/list/widget'],
        type='json',
        methods=['POST'],
        auth="user",
    )
    def list_dashboard_widget_request(self, **kwargs):
        values = dict(kwargs)
        dashboard_id = request.env['reporting.dashboard'].search(
            [('user_id', '=', request.uid), ('id', '=', int(values['id']))], limit=1
        )
        data = []
        for widget_line in dashboard_id.widget_line_ids:
            data.append(widget_line.get_dict())
        return json.dumps(data)

    @http.route(
        [
            '/lgf_reporting_app/dashboard/<string:dashboard_id>/add/widget/<string:widget_id>/sequence/<string:sequence>'
        ],
        type='json',
        methods=['POST'],
        auth="user",
    )
    def add_widget_to_dashboard(self, **kwargs):
        values = dict(kwargs)
        dashboard_id = request.env['reporting.dashboard'].search(
            [('user_id', '=', request.uid), ('id', '=', int(values['dashboard_id']))],
            limit=1,
        )
        dashboard_id.add_widget(int(values['widget_id']), int(values['sequence']))
        return json.dumps([True])

    @http.route(
        [
            '/lgf_reporting_app/dashboard/<string:dashboard_id>/remove/widget/<string:line_id>'
        ],
        type='json',
        methods=['POST'],
        auth="user",
    )
    def remove_widget_from_dashboard(self, **kwargs):
        values = dict(kwargs)
        dashboard_id = request.env['reporting.dashboard'].search(
            [('user_id', '=', request.uid), ('id', '=', int(values['dashboard_id']))],
            limit=1,
        )
        dashboard_id.remove_widget(int(values['line_id']))
        return json.dumps([True])

    @http.route(
        [
            '/lgf_reporting_app/dashboard/<string:dashboard_id>/update/sequence/<string:sequence>'
        ],
        type='json',
        methods=['POST'],
        auth="user",
    )
    def update_dashboard_sequence(self, **kwargs):
        values = dict(kwargs)
        dashboard_id = request.env['reporting.dashboard'].search(
            [('user_id', '=', request.uid), ('id', '=', int(values['dashboard_id']))],
            limit=1,
        )
        dashboard_id.update({'sequence': int(values['sequence'])})
        dashboard_ids = request.env['reporting.dashboard'].search(
            [('user_id', '=', request.uid)], order='sequence asc'
        )
        i = 0
        for db_id in dashboard_ids:
            if i == 0:
                db_id.is_default = True
            else:
                db_id.is_default = False
            i += 1
        return json.dumps([True])

    @http.route(
        ['/lgf_reporting_app/line/<string:line_id>/update/sequence/<string:sequence>'],
        type='json',
        methods=['POST'],
        auth="user",
    )
    def update_dashboard_widget_sequence(self, **kwargs):
        values = dict(kwargs)
        line_id = request.env['reporting.dashboard.line'].search(
            [('id', '=', int(values['line_id']))], limit=1
        )
        line_id.update({'sequence': int(values['sequence'])})
        return json.dumps([True])
