import re

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class TeachingDegree(models.Model):
    _name = 'teaching.degree'
    _description = 'Degree of Teaching'
    _rec_name = 'year_degree'
    _order = 'year_degree DESC'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_ids = fields.Many2one('teaching.teaching', string='Employees', required=True, ondelete='cascade',
                                   unique=True)

    year_degree = fields.Integer("Year")
    degree = fields.Integer("Degree", required=True)
    antique_degree = fields.Integer("Antique Degree", required=True)
    date_in_degree = fields.Date("Date in degree")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done')
    ], string='Status', default='draft')

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.degree}-{record.year_degree}"
            result.append((record.id, name))
        return result

    _sql_constraints = [
        (
            'teaching_unique',
            'UNIQUE (employee_ids)',
            'The teaching is unique!'
        )
    ]

    @api.onchange('degree')
    def _check_only_number_in_degree(self):
        for record in self:
            if not re.match(r'^\d{1}$', str(record.degree)):
                raise ValidationError("The degree must contain only one digits")

    @api.onchange('antique_degree')
    def _check_only_number_in_antique_degree(self):
        for record in self:
            if not re.match(r'^\d{1}$', str(record.antique_degree)):
                raise ValidationError("The degree must contain only one digits")
