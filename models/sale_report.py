from odoo import models, fields

class SaleReport(models.Model):
    _inherit = 'sale.report'

    operational_area_id = fields.Many2one(
        'operational.area',
        string='Operational Area',
        readonly=True
    )

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['operational_area_id'] = "s.operational_area_id"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += ", s.operational_area_id"
        return res