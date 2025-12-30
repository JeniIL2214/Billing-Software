from odoo import models, fields

class SaleOrderQRWizard(models.TransientModel):
    _name = 'sale.order.qr.wizard'
    _description = 'QR Code Wizard'

    qr_image = fields.Binary("QR Code", readonly=True)
    total_amount = fields.Float("Total Amount", readonly=True)
