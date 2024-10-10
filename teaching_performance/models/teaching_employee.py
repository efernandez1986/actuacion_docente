import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TeachingEmployee(models.Model):
    _inherit = 'hr.employee'

    no_document = fields.Char('No.document', required=True, size=8)

    birth_date = fields.Date('Birthday')

    is_teaching = fields.Boolean('IsTeaching', default=True)

    @api.onchange('no_document')
    def _onchange_no_document(self):
        pattern = r'^\d{8}$'
        if self.no_document:
            if not re.match(pattern, self.no_document):
                raise ValidationError(
                    _('¡The document is just numbers and 8 digits..! Example: 12345678'))
