from odoo import models, fields

class CrmTeam(models.Model):
    _inherit = 'crm.team'

    operational_area_id = fields.Many2one(
        'operational.area',
        string='Operational Area',
        tracking=True,
        help='Assigns this sales team to a specific geographical or operational zone.'
    )
