from odoo import api, fields, models, _
from datetime import datetime, timedelta

import logging
_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order', 'abstract.approvable']
    _name = 'purchase.order'

    @api.multi
    def to_json(self):
        res = super(PurchaseOrder, self).to_json()
        res['currency'] = self.currency_id.name
        res['model'] = 'purchase.order'
        res['date'] = self.date_order
        res['amount_total'] = self.amount_total
        res['partner'] = self.partner_id.name
        res['report_template'] = 'purchase.report_purchasequotation'
        return res

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('waiting_approval', 'Waiting Approval'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
        ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')

    @api.multi
    def action_request_approval(self):
        self.state = 'waiting_approval'

    @api.model
    def get_waiting_for_approval_list(self):
        po_ids = self.env['purchase.order'].search([('state', '=', 'waiting_approval')])
        return po_ids

    @api.multi
    def json_approve(self):
        self.button_confirm()
        return {'status': self.state}

    @api.multi
    def json_refuse(self):
        self.reject_action('Rejected from APP by %s' % self.env.user.name)
        return {'status': self.state}