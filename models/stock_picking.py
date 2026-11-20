from odoo import models, fields, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    finance_approved = fields.Boolean(
        string='Finance Approved',
        related='sale_id.finance_approved',
        readonly=True
    )

    def button_validate(self):
        """ Override validation to block outbound deliveries if Finance hasn't approved """
        for picking in self:
            if picking.sale_id and picking.picking_type_id.code == 'outgoing':
                if not picking.sale_id.finance_approved:
                    raise UserError(_(
                        "Cannot validate Delivery Order '%s'. Finance payment verification and approval on Sales Order '%s' is required before inventory can be released."
                    ) % (picking.name, picking.sale_id.name))
        return super().button_validate()