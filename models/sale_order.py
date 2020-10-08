from odoo import api, fields, models, _
from datetime import datetime, timedelta

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = ['sale.order', 'abstract.approvable']
    _name = 'sale.order'

    @api.multi
    def to_json(self):
        res = super(SaleOrder, self).to_json()
        res['currency'] = self.pricelist_id.currency_id.name
        res['model'] = 'sale.order'
        res['date'] = self.date_order
        res['amount_total'] = self.amount_total
        res['partner'] = self.partner_id.name
        res['report_template'] = 'sale.report_saleorder'
        return res

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('waiting_approval', 'Waiting Approval'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    @api.multi
    def action_request_approval(self):
        self.state = 'waiting_approval'

    @api.model
    def get_waiting_for_approval_list(self):
        so_ids = self.env['sale.order'].search([('state', '=', 'waiting_approval')])
        return so_ids

    @api.multi
    def json_approve(self):
        status = self.action_confirm()
        return {'status': self.state}

    @api.multi
    def json_refuse(self):
        self.reject_action('Rejected from APP by %s' % self.env.user.name)
        return {'status': self.state}