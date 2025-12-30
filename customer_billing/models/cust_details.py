from email.policy import default

from odoo import models, fields, api, _


class ARSCatalogInvoice(models.Model):
    _inherit = 'res.partner'

    company_type_bill = fields.Selection([('customer', 'Customer'), ('vendor', 'Vendor'),
                                     ('c/v', 'Customer / Vendor')], string='Customer Type')
    reg_type = fields.Selection([('regist', 'Registered'), ('unregist', 'Un-Registered')], string='Registration Type')
    pan = fields.Char('Pan')
    dummy_space = fields.Char('dummy_space')
    bill_add_id = fields.Many2one('res.partner', 'Billing Address')
    land_mark = fields.Char('Land Mark')
    company_id = fields.Many2one('res.company', 'Company')

    # def _get_price_total_and_subtotal_model(self, price_unit=None, discount=None, product=None, quantity=None,
    #                                         product_uom=None, taxes=None, currency=None):
    #     self.ensure_one()
    #
    #     # Default values
    #     if price_unit is None:
    #         price_unit = self.price_unit
    #     if discount is None:
    #         discount = self.discount
    #     if product is None:
    #         product = self.product_id
    #     if quantity is None:
    #         quantity = self.product_uom_qty
    #     if product_uom is None:
    #         product_uom = self.product_uom
    #     if taxes is None:
    #         taxes = self.tax_id
    #     if currency is None:
    #         currency = self.order_id.currency_id
    #
    #     # 💡 Apply discount ONLY on unit price
    #     price_after_discount = price_unit - (price_unit * (discount / 100.0))
    #
    #     # 👉 Compute subtotal with discount applied
    #     subtotal = quantity * price_after_discount
    #
    #     # 👉 Taxes always computed on original price_unit (NO discount here)
    #     taxes_res = taxes._origin.compute_all(
    #         price_unit,  # original price, no discount
    #         currency,
    #         quantity,
    #         product=product,
    #         partner=self.order_id.partner_shipping_id,
    #     )
    #
    #     return {
    #         'price_subtotal': subtotal,
    #         'price_total': subtotal + sum(t.get('amount', 0.0) for t in taxes_res.get('taxes', [])),
    #         'price_tax': sum(t.get('amount', 0.0) for t in taxes_res.get('taxes', [])),
    #     }





# from odoo import models, fields, api
#
# class ARSSaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     hsn_code = fields.Char('HSN/SAN Code')
#     product_uom_id = fields.Many2one('uom.uom', string='UOM')
#     discount = fields.Float(string="Discount Amount")  # amount discount, not %
#
    # @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    # def _compute_amount(self):
    #     """
    #     Override to compute subtotal considering discount as amount.
    #     """
    #     for line in self:
    #         # effective price after discount
    #         price_after_discount = line.price_unit - line.discount
    #
    #         # safeguard: price cannot be negative
    #         if price_after_discount < 0:
    #             price_after_discount = 0.0
    #
    #         taxes = line.tax_id.compute_all(
    #             price_after_discount,
    #             currency=line.order_id.currency_id,
    #             quantity=line.product_uom_qty,
    #             product=line.product_id,
    #             partner=line.order_id.partner_shipping_id,
    #         )
    #
    #         line.update({
    #             'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
    #             'price_total': taxes['total_included'],
    #             'price_subtotal': taxes['total_excluded'],
    #         })