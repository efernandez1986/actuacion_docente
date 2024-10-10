import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.teaching_performance.utils import _is_date_valid_today

from datetime import date, datetime


class TeachingTeaching(models.Model):
    _name = 'teaching.teaching'
    _description = 'Information of Teaching'
    _rec_name = 'employee_id'
    _order = 'employee_id ASC'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    record_id = fields.One2many(comodel_name='teaching.record', inverse_name='teaching_id', string='Record')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', ondelete='restrict', required=True,
                                  domain="[('is_teaching', '=', True)]")
    employee_no_document = fields.Char('No.document', related='employee_id.no_document')
    employee_birth = fields.Date('Birthday', related='employee_id.birth_date')
    employee_address = fields.Char('Address', related='employee_id.private_street')
    employee_phone = fields.Char('Phone', related='employee_id.private_phone')
    current_position = fields.Char('Current position', required=True)
    no_school = fields.Char('No.school', required=True)
    qualifying_title_date = fields.Date('Qualifying title date', required=True)
    first_effectiveness_date = fields.Date('First effectiveness date', required=True)
    entry_dgep_date = fields.Date('Entry DGEIP date')
    computation_years = fields.Integer('Computation years')
    computation_months = fields.Integer('Computation months')
    computation_days = fields.Integer('Computation days')
    years_computation = fields.Date('Years of computation', compute='_compute_years_computation', copy=True)
    observation_id = fields.One2many(comodel_name='teaching.observation', inverse_name='teaching_id',
                                     string='Observation')
    degree_id = fields.Many2one('teaching.degree', string='Degree', ondelete='set null')
    degree = fields.Integer('Degree', compute='_compute_degree', readonly=True)
    antique_degree = fields.Integer('Antique Degree', compute='_compute_antique_degree', readonly=True)
    score_id = fields.One2many(comodel_name='teaching.score', inverse_name='teaching_id')
    is_teaching = fields.Boolean('Is Teaching')

    @api.model
    def create(self, vals):
        result = super(TeachingTeaching, self).create(vals)
        result.is_teaching = True
        vals_degree = {
            'employee_ids': result.id,
            'year_degree': fields.Datetime.now().year,
            'degree': result.degree,
            'antique_degree': result.antique_degree,
            'date_in_degree': fields.Date.today()
        }
        degree_id = self.env['teaching.degree'].create(vals_degree)
        result.degree_id = degree_id
        return result

    def write(self, vals):
        super(TeachingTeaching, self).write(vals)
        if 'computation_years' in vals:
            degree = self.env['teaching.degree'].search([('employee_ids', '=', self.ids)])
            if degree:
                degree.write({'degree': self.degree, 'antique_degree': self.antique_degree})

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            employee = self.env['teaching.teaching'].search([('employee_id', '=', self.employee_id.id)])
            if self.employee_id.no_document:
                if employee:
                    raise ValidationError(
                        _(f'The employee ({employee.employee_id.name} - {employee.employee_id.no_document}), is register with teaching, select other that not is register.'))
            else:
                raise ValidationError(
                    _(f'The employee ({employee.employee_id.name}), does not have any documents.'))

    @api.onchange('no_school')
    def _onchange_no_school(self):
        pattern = r'^\d+$'
        if self.no_school:
            if not re.match(pattern, self.no_school):
                raise ValidationError(
                    _('¡The no school is just numbers! Please'))

    @api.onchange('entry_dgep_date', 'qualifying_title_date')
    def _onchange_date_entry_dgep_date_qualifying_title_date(self):
        for record in self:
            if record.entry_dgep_date and record.qualifying_title_date:
                if record.entry_dgep_date > record.qualifying_title_date:
                    raise ValidationError(
                        _('The date of entry must be less than the date of the qualifying title.'))

    @api.onchange('entry_dgep_date', 'first_effectiveness_date')
    def _onchange_date_entry_dgep_date_first_effectiveness_date(self):
        for record in self:
            if record.entry_dgep_date and record.first_effectiveness_date:
                if record.entry_dgep_date > record.first_effectiveness_date:
                    raise ValidationError(
                        _('The entry date must be less than the date of first effectiveness.'))

    @api.onchange('entry_dgep_date')
    def _onchange_date_entry_dgep_date(self):
        for record in self:
            if record.entry_dgep_date and not _is_date_valid_today(record.entry_dgep_date):
                raise ValidationError(
                    _("It sounds like you've chosen a future date. Please select a date no later than today"))

    @api.onchange('qualifying_title_date')
    def _onchange_date_qualifying_title_date(self):
        for record in self:
            if record.qualifying_title_date and not _is_date_valid_today(record.qualifying_title_date):
                raise ValidationError(
                    _("It sounds like you've chosen a future date. Please select a date no later than today")) @ api.onchange(
                    'entry_dgep_date')

    @api.onchange('first_effectiveness_date')
    def _onchange_date_first_effectiveness_date(self):
        for record in self:
            if record.first_effectiveness_date and not _is_date_valid_today(record.first_effectiveness_date):
                raise ValidationError(
                    _("It sounds like you've chosen a future date. Please select a date no later than today"))

    def _compute_years_computation(self):
        date_string = f'28/02/{date.today().year}'
        if not self.years_computation:
            self.years_computation = datetime.strptime(date_string, '%d/%m/%Y').date()

    def multiply_four(self, number):
        return number % 4 == 0

    @api.depends('computation_years')
    def _compute_degree(self):
        for record in self:
            if record.computation_years:
                if record.computation_years < 4:
                    record.degree = 1

                if record.computation_years < 29:
                    if self.multiply_four(record.computation_years):
                        record.degree = record.computation_years / 4
                    else:
                        record.degree = (record.computation_years / 4) + 1
                else:
                    record.degree = 7
            else:
                record.degree = 0

    @api.depends('computation_years')
    def _compute_antique_degree(self):
        for record in self:
            if record.computation_years:
                if record.computation_years < 4:
                    record.antique_degree = record.computation_years

                if record.computation_years < 29:
                    if self.multiply_four(record.computation_years):
                        record.antique_degree = 4
                    else:
                        record.antique_degree = record.computation_years % 4
                else:
                    record.antique_degree = record.computation_years - 24
            else:
                record.antique_degree = 0
