from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TeachingRecord(models.Model):
    _name = 'teaching.record'
    _description = 'Record of Teaching'
    _rec_name = 'title'
    _order = 'title ASC'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title = fields.Char('Record', required=True)
    degree_date = fields.Date('Date degree or ending')
    teaching_id = fields.Many2one('teaching.teaching', string='Teaching')
    teaching_name = fields.Char('Teaching Name', related='teaching_id.employee_id.name')