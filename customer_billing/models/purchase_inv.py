from odoo import models, fields, api, _


class ARSPurcahseInvoice(models.Model):
    _inherit = 'purchase.order'

    address = fields.Text('Address')
    contact_per = fields.Char('Contact Person')
    phone_no = fields.Char('Phone')
    gstin = fields.Char('GSTIN')
    pan = fields.Char('Pan')
    rev_change = fields.Selection([('y', 'Yes'), ('n', 'No')], string='Rev.Change')
    use_same_shipping = fields.Boolean(string="Use Same Shipping Address", default=True)
    shipping_address = fields.Text(string="Shipping Address")
    place_of_sup = fields.Char('Place of Supply')

    inv_type = fields.Selection([('g', 'General Invoice'), ('r', 'Regular Invoice')])
    seq_no = fields.Char('Sequence No.')
    purchase_inv_no = fields.Char('Purchase Invoice No.')
    date = fields.Date('Date', default=lambda self: fields.Datetime.now())
    chal_no = fields.Char('Challan No.')
    chal_date = fields.Date('Challan Date')
    lr_no = fields.Char('L.R. No.')
    eway_no = fields.Char('E-Way No.')
    entry_date = fields.Date('Entry Date')
    delivery = fields.Selection([('hd', 'Hand Delivery'), ('t/r', 'Transport/Road - Regular'), ('r/o', 'Road - Over Dimensional Cargo')], string='Delivery')
    due_date = fields.Date(string="Due Date")
    title = fields.Char('Title')
    details = fields.Char('Details')
    remark = fields.Text('Remarks')
    x_grand_total = fields.Char('x_grand_total')
    amount_total_words = fields.Char(compute="_compute_amount_total_words")
    payment_type = fields.Selection([
        ('credit', 'Credit'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('online', 'Online'),
    ], string="Payment Type")
    payment_rec = fields.Char('Payment Received')

    @api.depends('amount_total')
    def _compute_amount_total_words(self):
        for sale in self:
            sale.amount_total_words = sale.currency_id.amount_to_text(sale.amount_total)


class ARSPurchaseInvoiceLine(models.Model):
    _inherit = 'purchase.order.line'

    hsn_code = fields.Char('HSN/SAN Code', related='product_id.product_tmpl_id.hsn_code', store=True)
    product_uom_id = fields.Many2one('uom.uom', string='UOM')
    discount = fields.Float(string="Discount")
    cess_id = fields.Many2one('account.tax', 'CESS')



class ProductProductBSS(models.Model):
    _inherit = "product.template"

    hsn_code = fields.Char('HSN/SAN Code')


    #
    # cess_id = fields.Many2many('account.tax', 'product_taxes_rel', 'prod_id', 'tax_id',
    #                             string="CESS Tax",
    #                             domain=[('type_tax_use', '=', 'sale')],
    #                             default=lambda
    #                                 self: self.env.companies.account_sale_tax_id or self.env.companies.root_id.sudo().account_sale_tax_id,
    #                             )
