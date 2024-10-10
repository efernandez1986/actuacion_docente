from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError, ValidationError


class ScoreWizard(models.TransientModel):
    _name = 'teaching.score.wizard'
    _description = 'Score wizard'

    teaching_id = fields.Many2one('teaching.teaching', string='Teaching')
    employee_no_document = fields.Char('No.document')

    @api.onchange('no_document')
    def _onchange_no_document(self):
        pattern = r'^\d{8}$'
        if self.no_document:
            if not re.match(pattern, self.no_document):
                raise ValidationError(
                    _('¡The document is just numbers and 8 digits..! Example: 12345678'))

    # Lonna Y Lestapi Dreke 2024
    def action_show_score(self):
        datas = self

        if self.teaching_id:
            datas = self.teaching_id

        if self.employee_no_document:
            datas = self.env['teaching.teaching'].search([('employee_id.no_document', '=', self.employee_no_document)])

        if not self.employee_no_document and self.teaching_id:
            raise UserError(_('You must provide an employee number or select a teaching record.'))

        data = {
            'data': datas
        }

        return self.env.ref('import_management.report_container_xlsx').report_action(self, data=data)
