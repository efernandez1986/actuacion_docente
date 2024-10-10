from odoo import fields, models, api


class TeachingObservation(models.Model):
    _name = 'teaching.observation'
    _description = 'Observation of Teaching'
    _rec_name = 'teaching_id'
    _order = 'teaching_id ASC'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    teaching_id = fields.Many2one('teaching.teaching', string='Teaching', options={'no_create': True}, required=True)
    teaching_observation = fields.Text('Observation', size=200, required=True)