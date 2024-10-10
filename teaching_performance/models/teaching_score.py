from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TeachingScore(models.Model):
    _name = 'teaching.score'
    _description = 'Score of Teaching'
    _rec_name = 'year_score'
    _order = 'year_score DESC'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    teaching_id = fields.Many2one('teaching.teaching', string='Teaching')
    employee_no_document = fields.Char('No.document', related='teaching_id.employee_id.no_document')
    employee_degree = fields.Integer('Degree', related='teaching_id.degree_id.degree')
    employee_ant_degree = fields.Integer('Degree', related='teaching_id.degree_id.antique_degree')
    year_score = fields.Char('Year score', required=True, size=4)
    school = fields.Char('No.school', required=True)
    department = fields.Char(string='Department', required=True)
    character_position = fields.Char(string='Character of the position', required=True)
    teaching_performance_qualification = fields.Integer(string='Teaching performance qualification', required=True)
    computed_activity = fields.Float(string='Computed activity', required=True)
    qualified_antiquity= fields.Float(string='Qualified antiquity per score', required=True)
    total = fields.Float(string='Total score')
    total_average_tpq = fields.Float(string='Teaching performance qualification total')
    total_average_computed_activity = fields.Float(string='Computed activity total')
    total_average_qualified_activity = fields.Float(string='Qualified antiquity total')
    total_average_total = fields.Float(string='Total score total')
    antiquity_degree = fields.Float(string='Antiquity degree', required=True)
    observations = fields.Text(string='Observations')
    qualified_antiquity_resultant = fields.Float(string='Qualified antiquity resultant', required=True)

    @api.onchange('school')
    def _onchange_school(self):
        pattern = r'^\d+$'
        if self.school:
            if not re.match(pattern, self.school):
                raise ValidationError(
                    _('¡The school is just numbers! Please'))