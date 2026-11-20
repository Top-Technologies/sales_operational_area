from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})
    areas = env['operational.area'].with_context(active_test=False).search([
        ('company_id', '=', False),
    ])
    for area in areas:
        area.company_id = area.warehouse_id.company_id or env.ref('base.main_company')
