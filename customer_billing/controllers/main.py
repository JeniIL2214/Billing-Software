# controllers/invoice_kpi_dashboard.py
from odoo import http
from odoo.http import request

class InvoiceKPIDashboardController(http.Controller):

    @http.route('/invoice_kpi_dashboard/data', type='json', auth='user')
    def get_kpi_data(self):
        return request.env['invoice.kpi.dashboard'].sudo().get_invoice_kpis()
