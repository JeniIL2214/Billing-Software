from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import re
from datetime import datetime, timedelta, date
import qrcode
import base64
import barcode
from barcode.writer import ImageWriter
from io import BytesIO

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import qrcode
from io import BytesIO

import json
import logging

_logger = logging.getLogger(__name__)


class ARSSalesInvoice(models.Model):
    _inherit = 'sale.order'
    _description = 'Custom the sale Order'

    customer_gst = fields.Char(related="partner_id.vat", string="GST Number", readonly=False)
    customer_pan = fields.Char(related="partner_id.pan", string="Pan", readonly=False)
    customer_phone = fields.Char(related="partner_id.phone", string="Phone", readonly=False)
    customer_email = fields.Char(related="partner_id.email", string="Email", readonly=False)
    rev_change = fields.Selection([('y', 'Yes'), ('n', 'No')], string='Rev.Change', default='n')
    use_same_shipping = fields.Boolean(string="Use Same Shipping Address", default=True)
    shipping_address = fields.Text(string="Shipping Address")
    place_of_sup = fields.Char('Place of Supply')
    date = fields.Datetime('Date', default=lambda self: fields.Datetime.now())
    contact_per = fields.Char('Contact Person')

    inv_type = fields.Selection([('g', 'General Invoice'), ('r', 'Regular Invoice')], string='Invoice Type', default='g')
    inv_no = fields.Char('Invoice No.', compute="_compute_inv_no", store=True)
    inv_date = fields.Date('Date', default=lambda self: fields.Datetime.now())
    # chal_no = fields.Char('Challan No.')
    challan_ids = fields.One2many(
        'sale.challan',
        'sale_order_id',
        string='Challan Numbers'
    )
    chal_date = fields.Date('Challan Date')
    po_no = fields.Char('P.O. No.', copy=False)
    po_date = fields.Date('P.O Date', copy=False)
    lr_no = fields.Char('L.R. No.')
    eway_no = fields.Char('E-Way No.')
    delivery = fields.Selection([('hd', 'Hand Delivery'), ('t/r', 'Transport/Road - Regular'), ('r/o', 'Road - Over Dimensional Cargo')], string='Delivery',
                                default='hd')
    due_date = fields.Date(string="Due Date")

    # bank_id = fields.Many2one(
    #     'res.partner.bank',
    #     string="Bank Account",
    #     domain="[('partner_id', '=', partner_id)]",
    # )
    # bank_acc_number = fields.Char(string="Account Number")
    # bank_bic = fields.Char(string="Bank Short Name")
    # bank_name = fields.Char(string="Bank Name")

    title = fields.Char('Title')
    details = fields.Text('Details')
    remark = fields.Text('Remarks')
    x_grand_total = fields.Char('x_grand_total')
    amount_total_words = fields.Char(compute="_compute_amount_total_words")
    payment_type = fields.Selection([
        ('credit', 'Credit'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('online', 'Online'),
        # ('bank', 'Bank'),
    ], string="Payment Type")
    payment_rec = fields.Monetary(string="Payment Received")
    payment_remark = fields.Char('Remarks')
    credit_payment = fields.Monetary("Credit Payment")
    remaining_payment = fields.Monetary("Remaining Payment", compute="_compute_remaining_payment")
    online_ref = fields.Char("Online Reference")

    total_challan_amt = fields.Monetary(
        string='Total Challan Amount',
        compute='_compute_total_challan_amt',
        store=True,
        currency_field='currency_id'
    )

    remaining_challan_amt = fields.Monetary(
        string='Remaining Challan Amount',
        compute='_compute_remaining_challan_amt',
        store=False,  # no need to store
        currency_field='currency_id'
    )

    @api.depends('amount_total', 'challan_ids.challan_amt')
    def _compute_total_challan_amt(self):
        for order in self:
            order.total_challan_amt = sum(order.challan_ids.mapped('challan_amt'))

    @api.depends('amount_total', 'total_challan_amt')
    def _compute_remaining_challan_amt(self):
        for order in self:
            remaining = order.amount_total - order.total_challan_amt
            order.remaining_challan_amt = remaining if remaining > 0 else 0

    show_remaining_challan_amt = fields.Boolean(
        string="Show Remaining Challan Amount",
        compute='_compute_show_remaining_challan_amt'
    )

    @api.depends('remaining_challan_amt', 'payment_type')
    def _compute_show_remaining_challan_amt(self):
        for rec in self:
            rec.show_remaining_challan_amt = rec.remaining_challan_amt > 0 and rec.payment_type == 'cheque'







    # is_challan_amt_zero = fields.Boolean(
    #     string="Is Challan Amount Zero",
    #     compute='_compute_challan_amt_zero'
    # )
    #
    # @api.depends('remaining_challan_amt')
    # def _compute_challan_amt_zero(self):
    #     for rec in self:
    #         rec.is_challan_amt_zero = rec.remaining_challan_amt == 0


    # @api.depends('challan_ids.challan_amt')
    # def _compute_total_challan_amt(self):
    #     for order in self:
    #         order.total_challan_amt = sum(
    #             order.challan_ids.mapped('challan_amt')
    #         )



    # # Bank details
    # @api.onchange('payment_type', 'partner_id')
    # def _onchange_payment_type_bank(self):
    #     """ Auto-fetch bank_id only if payment_type is 'bank' """
    #     if self.payment_type == 'bank' and self.partner_id:
    #         bank = self.partner_id.bank_ids[:1]
    #         self.bank_id = bank.id if bank else False
    #         if bank:
    #             self.bank_acc_number = bank.acc_number
    #             self.bank_bic = bank.bank_bic
    #             self.bank_name = bank.bank_name
    #     else:
    #         self.bank_id = False
    #         self.bank_acc_number = False
    #         self.bank_bic = False
    #         self.bank_name = False
    #
    # @api.onchange('bank_id')
    # def _onchange_bank_id(self):
    #     """ If user manually changes bank_id, sync details """
    #     if self.bank_id:
    #         self.bank_acc_number = self.bank_id.acc_number
    #         self.bank_bic = self.bank_id.bank_bic
    #         self.bank_name = self.bank_id.bank_name
    #     else:
    #         self.bank_acc_number = False
    #         self.bank_bic = False
    #         self.bank_name = False



    # payment type  ///////////////
    @api.constrains('payment_type', 'online_ref')
    def _check_online_requirements(self):
        for order in self:
            if order.payment_type == 'online' and not order.online_ref:
                raise ValidationError("Online Reference is required when payment type is Online.")

    @api.depends('credit_payment', 'amount_total')
    def _compute_remaining_payment(self):
        for order in self:
            if order.payment_type == 'credit':
                order.remaining_payment = order.amount_total - order.credit_payment
            else:
                order.remaining_payment = 0.0

    # ////////////////

    # reset the value of payment type 0 /////////
    @api.onchange('payment_type')
    def _onchange_payment_type(self):
        """Clear payment fields when payment type changes"""
        if self.payment_type:
            # reset payment amounts to 0
            self.payment_rec = 0.0
            self.credit_payment = 0.0
            self.remaining_payment = 0.0
            self.online_ref = False
            self.payment_remark = False
            self.challan_ids = False
            self.chal_date = False

    #         ///////////////

    # validation phone & mail    ////

    @api.onchange('customer_email')
    def email_validation(self):
        match_customer_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if self.customer_email:
            if not re.match(match_customer_email, self.customer_email):
                raise UserError(f'{self.customer_email} is not a valid email')

    @api.constrains('customer_phone')
    def _check_phone_length(self):
        for rec in self:
            if rec.customer_phone:
                # Only allow exactly 10 digits
                if not re.fullmatch(r'^\d{10}$', rec.customer_phone):
                    raise ValidationError("Phone number must be exactly 10 digits (only numbers allowed).")

    @api.onchange('customer_phone')
    def _onchange_customer_phone_validate(self):
        if self.customer_phone and not re.fullmatch(r'^\d{10}$', self.customer_phone):
            warning = {
                'title': "Invalid Phone",
                'message': "Phone number must be exactly 10 digits.",
            }
            self.customer_phone = False
            return {'warning': warning}
    # //////////
    # po sequence & date

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Generate PO No if not provided
            if not vals.get('po_no'):
                vals['po_no'] = self.env['ir.sequence'].next_by_code('sale.order.po.no') or 'PO000'

            # Set PO Date if not provided
            if not vals.get('po_date'):
                vals['po_date'] = date.today()

        return super(ARSSalesInvoice, self).create(vals_list)


    # depends on phone number to get the exsisting customer

    @api.onchange('customer_phone')
    def _onchange_customer_phone(self):
        if self.customer_phone:
            partner = self.env['res.partner'].search([('phone', '=', self.customer_phone)], limit=1)
            if partner:
                self.partner_id = partner
            else:
                # Do NOT create a new partner here
                raise ValidationError(
                    f"Phone number {self.customer_phone} does not match any existing customer. "
                    f"Please create the customer in Contacts first."
                )
    # @api.onchange('customer_phone')
    # def _onchange_customer_phone(self):
    #     if self.customer_phone:
    #         partner = self.env['res.partner'].search([('phone', '=', self.customer_phone)], limit=1)
    #
    #         if partner:
    #             self.partner_id = partner
    #         else:
    #             # if not found, prepare a new customer (not saved until SO is saved)
    #             new_partner = self.env['res.partner'].create({
    #                 'name': ' ',
    #                 'phone': self.customer_phone,
    #                 'street': '',
    #                 'city': '',
    #             })
    #             self.partner_id = new_partner
    # //////////////////


    # //////////// challan number when have the payment type is cheque
    @api.constrains('payment_type', 'challan_ids', 'chal_date')
    def _check_cheque_requirements(self):
        for order in self:
            if order.payment_type == 'cheque':
                if not order.challan_ids:
                    raise ValidationError("Challan No is required when payment type is Cheque.")
                if not order.chal_date:
                    raise ValidationError("Challan Date is required when payment type is Cheque.")
    # ///////



    # validation for challon details
    @api.constrains('payment_type', 'challan_ids')
    def _check_challan_required(self):
        for rec in self:
            if rec.payment_type == 'cheque' and not rec.challan_ids:
                raise ValidationError("Please add at least one Challan Number.")

    # //////////// credit number when have the payment type is cheque
    @api.constrains('credit_payment')
    def _check_credit_requirements(self):
        for order in self:
            if order.payment_type == 'credit':
                if not order.credit_payment:
                    raise ValidationError("Credit Payment is required when payment type is Credit.")


    # ///////

        # //////////// credit number when have the payment type is cheque
        @api.constrains('cash')
        def _check_cash_requirements(self):
            for order in self:
                if order.payment_type == 'cash':
                    if not order.credit_payment:
                        raise ValidationError("Payment Received is required when payment type is Cash.")

        # ///////


    # //////////// bank details have been mandatory when have the payment type is online

    # @api.constrains('payment_type', 'bank_deta')
    # def _check_online_requirements(self):
    #     for order in self:
    #         if order.payment_type == 'online':
    #             if not order.bank_deta:
    #                 raise ValidationError("Bank Details is required when payment type is Online.")


    #//////////////

    # invoice number before and after
    @api.depends('name', 'invoice_ids.name')
    def _compute_inv_no(self):
        for order in self:
            so_name = order.name or ""
            # ensure we only take non-false invoice names
            inv_names_list = [inv_name for inv_name in order.invoice_ids.mapped("name") if inv_name]
            inv_names = ", ".join(inv_names_list) if inv_names_list else ""
            if inv_names:
                order.inv_no = f"{so_name} - {inv_names}"
            else:
                order.inv_no = so_name


    #////////

    # amount convert the words
    @api.depends('amount_total')
    def _compute_amount_total_words(self):
        for sale in self:
            sale.amount_total_words = sale.currency_id.amount_to_text(sale.amount_total)
    # /////////


    # if shipping is true
    @api.onchange('use_same_shipping', 'partner_id')
    def _onchange_use_same_shipping(self):
        if self.use_same_shipping:
            # copy customer address if available
            self.shipping_address = self.partner_id.contact_address or self.partner_id.street
        else:
            # clear it so user must fill
            self.shipping_address = False

#    QR Scanner function



    # def action_open_qr_wizard(self):
    #     self.ensure_one()
    #
    #     amount = self.credit_payment or 0.0
    #     if amount <= 0:
    #         raise UserError(_("Credit payment amount must be greater than zero."))
    #
    #     upi_id = "merchant@upi"
    #     merchant_name = "MyStore"
    #
    #     qr_string = f"upi://pay?pa={upi_id}&pn={merchant_name}&am={amount}&cu=INR"
    #
    #     qr = qrcode.QRCode(
    #         version=1,
    #         error_correction=qrcode.constants.ERROR_CORRECT_H,
    #         box_size=10,
    #         border=4
    #     )
    #     qr.add_data(qr_string)
    #     qr.make(fit=True)
    #     img = qr.make_image(fill_color="black", back_color="white")
    #
    #     buffer = BytesIO()
    #     img.save(buffer, format="PNG")
    #     qr_binary = base64.b64encode(buffer.getvalue())
    #
    #     wizard = self.env['sale.order.qr.wizard'].create({
    #         'qr_image': qr_binary,
    #         'total_amount': amount,
    #     })
    #
    #     return {
    #         'name': 'QR Code',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'sale.order.qr.wizard',
    #         'view_mode': 'form',
    #         'res_id': wizard.id,
    #         'target': 'new',
    #     }


# from odoo import models, fields, _
# from odoo.exceptions import UserError
# import base64
# import qrcode
# from io import BytesIO
#
#
# class SaleOrder(models.Model):
#     _inherit = 'sale.order'

    def action_open_qr_wizard(self):
        self.ensure_one()

        if self.credit_payment and self.credit_payment > 0:
            amount = self.credit_payment
        elif self.payment_rec and self.payment_rec > 0:
            amount = self.payment_rec
        elif self.total_challan_amt and self.total_challan_amt > 0:
            amount = self.total_challan_amt
        else:
            amount = self.amount_total

        if amount <= 0:
            raise UserError(_("Payment amount must be greater than zero."))

        upi_id = "merchant@upi"
        merchant_name = "MyStore"

        qr_string = f"upi://pay?pa={upi_id}&pn={merchant_name}&am={amount}&cu=INR"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )
        qr.add_data(qr_string)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_binary = base64.b64encode(buffer.getvalue())

        wizard = self.env['sale.order.qr.wizard'].create({
            'qr_image': qr_binary,
            'total_amount': amount,
        })

        return {
            'name': 'QR Code',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.qr.wizard',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new',
        }



#
#     def action_open_qr_wizard(self):
#         self.ensure_one()
#         total_amount = sum(line.price_total for line in self.order_line)
#
#         # UPI QR string
#         upi_id = "merchant@upi"  # replace with your UPI ID
#         merchant_name = "MyStore"  # merchant name
#         qr_string = f"upi://pay?pa={upi_id}&pn={merchant_name}&am={total_amount}&cu=INR"
#
#         # Generate QR
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_H,
#             box_size=10,
#             border=4
#         )
#         qr.add_data(qr_string)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")
#
#         buffer = BytesIO()
#         img.save(buffer, format="PNG")
#         qr_binary = base64.b64encode(buffer.getvalue())
#
#         wizard = self.env['sale.order.qr.wizard'].create({
#             'qr_image': qr_binary,
#             'total_amount': total_amount,
#         })
#         return {
#             'name': 'QR Code',
#             'type': 'ir.actions.act_window',
#             'res_model': 'sale.order.qr.wizard',
#             'view_mode': 'form',
#             'res_id': wizard.id,
#             'target': 'new',
#         }


# //////////////

# account invoice of sale order line

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()

        if self.payment_type == 'credit' and self.credit_payment:
            invoice_vals.update({
                'payment_received_amount': self.credit_payment
            })

        elif self.payment_type == 'cash' and self.payment_rec:
            invoice_vals.update({
                'payment_received_amount': self.payment_rec
            })

        elif self.payment_type == 'cheque' and self.total_challan_amt:
            invoice_vals.update({
                'payment_received_amount': self.total_challan_amt
            })

        return invoice_vals


class SaleChallan(models.Model):
    _name = 'sale.challan'
    _description = 'Customer Challan'

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        ondelete='cascade'
    )

    challan_no = fields.Char(
        string='Challan No.',
        required=True
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id
    )

    challan_amt = fields.Monetary(
        string="Amount",
        currency_field='currency_id'
    )





#

class ARSSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    hsn_code = fields.Char('HSN/SAN Code', related='product_id.product_tmpl_id.hsn_code', store=True)
    product_uom_id = fields.Many2one('uom.uom', string='UOM')
    discount = fields.Float(string="Discount")
    cess_id = fields.Many2one('account.tax', 'CESS')


class ProductTemplate(models.Model):
    _inherit = "product.template"


    cess_id = fields.Many2many('account.tax', 'product_taxes_rel', 'prod_id', 'tax_id',
                                string="CESS Tax",
                                domain=[('type_tax_use', '=', 'sale')],
                                default=lambda
                                    self: self.env.companies.account_sale_tax_id or self.env.companies.root_id.sudo().account_sale_tax_id,
                                )

    qr_code = fields.Binary("QR Code", compute="_generate_qr_code", store=True)
    barcode_image = fields.Binary("Barcode", compute="_compute_barcode_image", store=True)
    mfg_date = fields.Date('Manufacture Date')
    exp_date = fields.Date('Expiry Date')


    # QR CODE of product amount
    @api.depends('list_price')
    def _generate_qr_code(self):
        for rec in self:
            if rec.list_price:
                # UPI payment link
                upi_id = "merchant@upi"  # Replace with your UPI ID
                payee_name = "YourShop"
                note = rec.name
                amount = rec.list_price
                currency = "INR"

                upi_url = f"upi://pay?pa={upi_id}&pn={payee_name}&tn={note}&am={amount}&cu={currency}"

                # Create QR code with UPI URL
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=10,
                    border=4,
                )
                qr.add_data(upi_url)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                qr_image = base64.b64encode(buffer.getvalue())
                rec.qr_code = qr_image
            else:
                rec.qr_code = False


    # barcode generate

    @api.model
    def create(self, vals):
        # Auto-generate barcode if not provided
        if not vals.get("barcode"):
            seq = self.env["ir.sequence"].next_by_code("product.barcode")
            if not seq:
                raise UserError("Please configure the sequence 'product.barcode'.")
            vals["barcode"] = seq
        return super().create(vals)

    @api.depends("barcode")
    def _compute_barcode_image(self):
        for rec in self:
            if rec.barcode:
                try:
                    Code128 = barcode.get_barcode_class("code128")
                    code128 = Code128(rec.barcode, writer=ImageWriter())
                    buffer = BytesIO()
                    code128.write(buffer, options={
                        "module_width": 0.2,
                        "module_height": 4,
                        "font_size": 4,
                        "text_distance": 2,
                        "quiet_zone": 0.5
                    })
                    rec.barcode_image = base64.b64encode(buffer.getvalue())
                except Exception as e:
                    rec.barcode_image = False
                    _logger = self.env['ir.logging']
                    _logger.sudo().create({
                        'name': 'Barcode Error',
                        'type': 'server',
                        'dbname': self._cr.dbname,
                        'level': 'ERROR',
                        'message': f"Failed to generate barcode for {rec.name}: {e}",
                        'path': 'product.template._compute_barcode_image',
                        'func': '_compute_barcode_image',
                        'line': '0',
                    })
            else:
                rec.barcode_image = False

    # Method to fetch product details by barcode
    @api.model
    def get_product_details_by_barcode(self, barcode):
        product = self.search([('barcode', '=', barcode)], limit=1)
        if not product:
            return {'error': 'Product not found'}
        return {
            'name': product.name,
            'price': product.list_price,
            'mfg_date': str(product.mfg_date) if product.mfg_date else '',
            'exp_date': str(product.exp_date) if product.exp_date else '',
            'hsn_code': product.hsn_code or '',
        }
    # @api.depends("barcode")
    # def _compute_barcode_image(self):
    #     for rec in self:
    #         if rec.barcode:
    #             try:
    #                 Code128 = barcode.get_barcode_class("code128")
    #                 code128 = Code128(rec.barcode, writer=ImageWriter())
    #
    #                 buffer = BytesIO()
    #                 # control size with options
    #                 code128.write(buffer, options={
    #                     "module_width": 0.2,  # width of a single bar (default 0.2)
    #                     "module_height": 4,  # height of the bars (default 15)
    #                     "font_size": 4,  # text size (default 10)
    #                     "text_distance": 2,  # gap between barcode and text
    #                     "quiet_zone": 0.5  # margin on sides
    #                 })
    #
    #                 rec.barcode_image = base64.b64encode(buffer.getvalue())
    #             except Exception as e:
    #                 rec.barcode_image = False
    #                 print(f"Failed to generate barcode for {rec.name}: {e}")
    #         else:
    #             rec.barcode_image = False


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _sanitize_number(self, number):
        """Remove +91, spaces, dashes, keep only digits"""
        digits = re.sub(r'\D', '', number or "")
        if digits.startswith('91') and len(digits) > 10:
            digits = digits[2:]
        return digits

    # def _phone_format(self, number, country=None, company=None, **kwargs):
    #     """Bypass Odoo's phone_validation formatting"""
    #     return self._sanitize_number(number)

    @api.model
    def create(self, vals):
        if vals.get('mobile'):
            vals['mobile'] = self._sanitize_number(vals['mobile'])
        if vals.get('phone'):
            vals['phone'] = self._sanitize_number(vals['phone'])
        return super().create(vals)

    def write(self, vals):
        if vals.get('mobile'):
            vals['mobile'] = self._sanitize_number(vals['mobile'])
        if vals.get('phone'):
            vals['phone'] = self._sanitize_number(vals['phone'])
        return super().write(vals)


#
# class ResPartner(models.Model):
#     _inherit = "res.partner"
#
#     @api.constrains('phone')
#     def _check_phone_length(self):
#         for rec in self:
#             if rec.phone:
#                 # Allow only exactly 10 digits
#                 if not re.fullmatch(r'^\d{10}$', rec.phone):
#                     raise ValidationError("Phone number must be exactly 10 digits (only numbers allowed).")
#
#     @api.onchange('email')
#     def email_validation(self):
#         match_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
#         if self.email:
#             if not re.match(match_email, self.email):
#                 raise UserError(f'{self.email} is not a valid email')





class AccountMove(models.Model):
    _inherit = 'account.move'

    payment_received_amount = fields.Char(
        string="Payment Received"
    )

