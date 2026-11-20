from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class OperationalArea(models.Model):
    _name = 'operational.area'
    _description = 'Operational Area'

    name = fields.Char(string='Area Name', required=True)
    code = fields.Char(string='Area Code')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        index=True
    )
    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Assigned Warehouse',
        required=True,
        domain="[('company_id', '=', company_id)]",
        check_company=True,
        help='Warehouse responsible for fulfilling orders in this operational area.'
    )
    location_id = fields.Many2one(
        'stock.location',
        string='Default Stock Location',
        related='warehouse_id.lot_stock_id',
        readonly=True,
        store=True
    )

    @api.constrains('company_id', 'warehouse_id')
    def _check_warehouse_company(self):
        for area in self:
            if area.warehouse_id and area.warehouse_id.company_id != area.company_id:
                raise ValidationError(_(
                    "The warehouse '%(warehouse)s' must belong to the same company as "
                    "the operational area '%(area)s'.",
                    warehouse=area.warehouse_id.display_name,
                    area=area.name,
                ))
