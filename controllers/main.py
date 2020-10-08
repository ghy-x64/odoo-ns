import odoo.http as http
from odoo import SUPERUSER_ID
from odoo import _
from odoo.http import request
from odoo.exceptions import AccessError, UserError
import logging
_logger = logging.getLogger(__name__)
import json
# import xmlrpclib

class RequestController(http.Controller):
    
    @http.route(['/api/waiting_approval_list'], type='json', methods=['POST'], auth="user")
    def waiting_approval_list(self, **kwargs):
        if request.env.user.name == 'demo':
            return json.dumps([{
                'name': 'DEMOSO',
                'id': 500000,
                'username': 'demo',
                'dept': 'demo Dept',
                'company': 'demoCompany',
                'last_edit_date': '2020-01-01 00:00:00',
                'currency' : 'USD',
                'model' : 'sale.order',
                'date' : '2020-01-01 00:00:00',
                'amount_total' : 10000,
                'partner' : 'Demo customer',
                'report_template' : 'sale.report_saleorder',
            }])
        else:
            values = dict(kwargs)
            data = request.env['abstract.approvable'].get_waiting_for_approval_json()
            json_dump = json.dumps(data)
            return json_dump

    @http.route(['/api/approve/<string:model>/<string:id>'], type='json', auth="user", methods=['POST'])
    def approve_document(self, **kwargs):
        if request.env.user.name == 'demo':
            return json.dumps({'state':'confirmed'})
        else:
            values = dict(kwargs)
            values['id'] = int(values['id'])
            obj_id = request.env[values['model']].browse([int(values['id'])])
            result = obj_id.json_approve()
            return json.dumps(result)

    @http.route(['/api/refuse/<string:model>/<string:id>'], type='json', auth="user", methods=['POST'])
    def refuse_document(self, **kwargs):
        if request.env.user.name == 'demo':
            return json.dumps({'state':'confirmed'})
        else:
            values = dict(kwargs)
            values['id'] = int(values['id'])
            obj_id = request.env[values['model']].browse([int(values['id'])])
            result = obj_id.json_refuse()
            return json.dumps(result)




