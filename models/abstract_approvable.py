import logging
import openerp.addons.decimal_precision as dp
from datetime import datetime, date, timedelta
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import models, fields, api, _
from lxml import etree

_logger = logging.getLogger(__name__)

    
class AbstractApprovable(models.AbstractModel):
    _name = "abstract.approvable"

    @api.multi
    def to_json(self):
        return {
            'name': self.name,
            'id': self.id,
            'username': self.user_id.name,
            'company': self.company_id.name,
            'last_edit_date': self.write_date,
            }

    @api.model
    def get_waiting_for_approval_json(self):
        children_model = ['sale.order', 'purchase.order']
        doc_ids = []
        for child in children_model:
            doc_ids += self.env[child].get_waiting_for_approval_list()
        data = []
        for doc in doc_ids:
            data.append(doc.to_json())
        data = sorted(data, key=lambda k: k['last_edit_date']) 
        return data



    

