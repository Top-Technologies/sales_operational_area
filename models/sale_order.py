from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    operational_area_id = fields.Many2one(
        'operational.area',
        string='Operational Area',
        compute='_compute_operational_area',
        store=True,
        readonly=False,
        domain="[('company_id', '=', company_id)]",
        tracking=True,
        help='Operational area linked to the selected sales team.'
    )
    finance_approved = fields.Boolean(
        string='Finance Approved',
        default=False,
        tracking=True,
        copy=False,
        help='Indicates that Finance has verified payment and approved inventory release.'
    )

    def action_finance_approve(self):
        """ Button action for Finance to approve payment """
        for order in self:
            order.finance_approved = True
            order.message_post(body=_("Finance payment verification completed. Inventory release approved."))

    def action_finance_unapprove(self):
        """ Button action for Finance to revoke payment approval """
        for order in self:
            done_pickings = order.picking_ids.filtered(lambda p: p.picking_type_id.code == 'outgoing' and p.state == 'done')
            if done_pickings:
                raise UserError(_("Cannot revoke approval because delivery order '%s' has already been validated and shipped.") % done_pickings[0].name)
            order.finance_approved = False
            order.message_post(body=_("Finance payment approval has been revoked. Delivery validation is now blocked."))

    @api.depends('team_id', 'company_id')
    def _compute_operational_area(self):
        for order in self:
            area = order.team_id.operational_area_id
            if area and area.company_id == order.company_id:
                order.operational_area_id = area
            elif not order.team_id or order.operational_area_id.company_id != order.company_id:
                order.operational_area_id = False

    @api.onchange('team_id')
    def _onchange_team_id_warehouse(self):
        """ Automatically set warehouse and operational area based on sales team """
        area = self.team_id.operational_area_id
        if area and area.company_id == self.company_id:
            self.operational_area_id = area.id
            if area.warehouse_id:
                self.warehouse_id = area.warehouse_id

    @api.onchange('operational_area_id')
    def _onchange_operational_area_id(self):
        """ Automatically update warehouse if operational area changes directly """
        if self.operational_area_id and self.operational_area_id.company_id == self.company_id:
            if self.operational_area_id.warehouse_id:
                self.warehouse_id = self.operational_area_id.warehouse_id