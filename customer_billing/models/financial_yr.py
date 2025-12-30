from odoo import models
from odoo.http import request
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date
from odoo.exceptions import UserError, AccessError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class FinancialYear(models.Model):
    _name = 'financial.year.master'
    _description = 'FY Master'
    # _rec_name = 'name'

    name = fields.Char(string="Year")


class ResUsers(models.Model):
    _inherit = 'res.users'

    financial_year_id = fields.Many2one(
        'financial.year.master',
        string='Current Year'
    )

    allowed_financial_year_id = fields.Many2many('financial.year.master','branch_user_rel','user_id','branch_id',string='Allowed Financial Year',
                                          ondelete='cascade',store=True)

    def write(self, vals):
        # Case 1: If only 'company_id' is being changed, reset 'branch_id'
        if 'company_id' in vals and len(vals) == 1:
            vals['financial_year_id'] = False

        # Case 2: Logic for allowed_branch_ids and branch_id consistency
        if 'allowed_financial_year_id' in vals or 'financial_year_id' in vals:
            self.env.user.clear_caches()

        if 'allowed_financial_year_id' in vals:
            for user in self:
                new_allowed_branches = vals.get('allowed_financial_year_id')
                if isinstance(new_allowed_branches, list) and new_allowed_branches and new_allowed_branches[0][0] == 6:
                    allowed_ids = set(new_allowed_branches[0][2])
                    if user.financial_year_id and user.financial_year_id.id not in allowed_ids:
                        vals.setdefault('financial_year_id', False)

        return super(ResUsers, self).write(vals)


# {
#   "version": 21,
#   "sheets": [
#     {
#       "id": "a7cd7db1-9407-4895-82f2-7657102c7688",
#       "name": "Dashboard",
#       "colNumber": 7,
#       "rowNumber": 69,
#       "rows": {
#         "6": { "size": 40 },
#         "22": { "size": 40 }
#       },
#       "cols": {
#         "0": { "size": 225 },
#         "1": { "size": 150 },
#         "2": { "size": 100 },
#         "3": { "size": 50 },
#         "4": { "size": 225 },
#         "5": { "size": 150 },
#         "6": { "size": 100 }
#       },
#       "merges": [
#
#       ],
#       "cells": {
#         "A7": {
#           "content": "[Invoiced by Month](odoo://view/{\"viewType\":\"graph\",\"action\":{\"domain\":[\"&\",[\"state\",\"not in\",[\"draft\",\"cancel\"]],\"|\",[\"move_type\",\"=\",\"out_invoice\"],[\"move_type\",\"=\",\"out_refund\"]],\"context\":{\"group_by\":[\"invoice_date\"],\"graph_measure\":\"price_subtotal\",\"graph_mode\":\"line\",\"graph_groupbys\":[\"invoice_date:month\"]},\"modelName\":\"account.invoice.report\",\"views\":[[false,\"graph\"],[false,\"pivot\"],[false,\"search\"]]},\"threshold\":0,\"name\":\"Invoices Analysis\",\"positional\":true})"
#         }
#       },
#       "styles": {
#         "A7": 1
#       },
#       "formats": {},
#       "borders": {
#         "A7:G7": 1
#       },
#       "conditionalFormats": [
#         {
#           "rule": {
#             "type": "DataBarRule",
#             "color": 16708338,
#             "rangeValues": "G25:G34"
#           },
#           "id": "3913485d-dafc-481c-81cb-5de1007c2beb",
#           "ranges": ["A25:A34"]
#         },
#         {
#           "rule": {
#             "type": "DataBarRule",
#             "color": 16775149,
#             "rangeValues": "C38:C47"
#           },
#           "id": "4b1963a5-6d8a-48e7-baed-15a352bd88f2",
#           "ranges": ["A38:A47"]
#         },
#         {
#           "rule": {
#             "type": "DataBarRule",
#             "color": 15726335,
#             "rangeValues": "G38:G47"
#           },
#           "id": "8a8b5811-25a7-4334-8a9a-64549dfcd3b7",
#           "ranges": ["E38:E47"]
#         },
#         {
#           "rule": {
#             "type": "DataBarRule",
#             "color": 15531509,
#             "rangeValues": "C51:C60"
#           },
#           "id": "c8b9e9e0-18e0-45ed-8aae-86f555e4fc4d",
#           "ranges": ["A51:A60"]
#         },
#         {
#           "rule": {
#             "type": "DataBarRule",
#             "color": 16708338,
#             "rangeValues": "G51:G60"
#           },
#           "id": "4ebb2a3e-fd9b-4627-a543-d3523f719908",
#           "ranges": ["E51:E60"]
#         }
#       ],
#       "figures": [
#         {
#           "id": "5ea5dd7f-9f83-4482-a2bb-2ec72ab35912",
#           "x": 0,
#           "y": 178,
#           "width": 1000,
#           "height": 345,
#           "tag": "chart",
#           "data": {
#             "title": { "text": "" },
#             "background": "#FFFFFF",
#             "legendPosition": "none",
#             "metaData": {
#               "groupBy": ["invoice_date:month"],
#               "measure": "price_subtotal",
#               "order": null,
#               "resModel": "account.invoice.report",
#               "mode": "line"
#             },
#             "searchParams": {
#               "comparison": null,
#               "context": { "group_by": ["invoice_date"] },
#               "domain": [
#                 "&",
#                 ["state", "not in", ["draft", "cancel"]],
#                 "|",
#                 ["move_type", "=", "out_invoice"],
#                 ["move_type", "=", "out_refund"]
#               ],
#               "groupBy": ["invoice_date"],
#               "orderBy": []
#             },
#             "type": "odoo_line",
#             "verticalAxisPosition": "left",
#             "stacked": false,
#             "fillArea": true,
#             "fieldMatching": {
#               "757a1b4b-e339-4879-beb6-9851050387cf": {
#                 "chain": "invoice_date",
#                 "type": "date",
#                 "offset": 0
#               }
#             }
#           }
#         },
#         {
#           "id": "1aeea7b2-900b-4067-b8ad-3e4772c54028",
#           "x": 0,
#           "y": 11,
#           "width": 200,
#           "height": 109,
#           "tag": "chart",
#           "data": {
#             "baselineColorDown": "#DC6965",
#             "baselineColorUp": "#00A04A",
#             "baselineMode": "text",
#             "title": { "text": "Invoiced", "color": "#434343", "bold": true },
#             "type": "scorecard",
#             "background": "#EFF6FF",
#             "baseline": "Data!C11",
#             "baselineDescr": "unpaid",
#             "keyValue": "Data!C1",
#             "humanize": false
#           }
#         },
#         {
#           "id": "bdfb27d0-5902-4a2a-9b7e-514a6625578c",
#           "x": 210,
#           "y": 11,
#           "width": 200,
#           "height": 109,
#           "tag": "chart",
#           "data": {
#             "baselineColorDown": "#DC6965",
#             "baselineColorUp": "#00A04A",
#             "baselineMode": "text",
#             "title": {
#               "text": "Average Invoice",
#               "color": "#434343",
#               "bold": true
#             },
#             "type": "scorecard",
#             "background": "#EFF6FF",
#             "baseline": "Data!C3",
#             "baselineDescr": "Invoices",
#             "keyValue": "Data!C2",
#             "humanize": false
#           }
#         },
#         {
#           "id": "b1673523-d139-47fb-b5ea-9e4f969aacb6",
#           "x": 419,
#           "y": 11,
#           "width": 200,
#           "height": 109,
#           "tag": "chart",
#           "data": {
#             "baselineColorDown": "#DC6965",
#             "baselineColorUp": "#00A04A",
#             "baselineMode": "difference",
#             "title": { "text": "DSO", "color": "#434343", "bold": true },
#             "type": "scorecard",
#             "background": "#FEF2F2",
#             "baselineDescr": "in current year",
#             "keyValue": "Data!C10",
#             "humanize": false
#           }
#         }
#       ],
#       "tables": [],
#       "areGridLinesVisible": true,
#       "isVisible": true,
#       "headerGroups": { "ROW": [], "COL": [] },
#       "dataValidationRules": [],
#       "comments": {}
#     },
#     {
#       "id": "685cb5c3-4acb-45eb-8000-99e1af15b3ed",
#       "name": "Data",
#       "colNumber": 26,
#       "rowNumber": 107,
#       "rows": { "3": { "size": 23 } },
#       "cols": { "0": { "size": 142 }, "1": { "size": 128 } },
#       "merges": [],
#       "cells": {
#         "A1": { "content": "=_t(\"KPI - Income\")" },
#         "A2": { "content": "=_t(\"KPI - Average Invoice\")" },
#         "A3": { "content": "=_t(\"KPI - Invoice Count\")" },
#         "A4": { "content": "=_t(\"Current year\")" },
#         "A5": { "content": "=_t(\"Receivable\")" },
#         "A6": { "content": "=_t(\"Income\")" },
#         "A7": { "content": "=_t(\"COGS\")" },
#         "A8": { "content": "=_t(\"Revenue\")" },
#         "A9": { "content": "=_t(\"# days\")" },
#         "A10": { "content": "=_t(\"KPI - DSO\")" },
#         "A11": { "content": "=_t(\"KPI - Unpaid Invoices\")" },
#         "B1": { "content": "=PIVOT.VALUE(5,\"price_subtotal\")" },
#         "B2": { "content": "=IFERROR(PIVOT.VALUE(6,\"price_subtotal\")/B3)" },
#         "B3": { "content": "=PIVOT.VALUE(6,\"move_id\")" },
#         "B4": { "content": "=YEAR(TODAY())" },
#         "B5": {
#           "content": "=ODOO.BALANCE(ODOO.ACCOUNT.GROUP(\"asset_receivable\"),$B$4)"
#         },
#         "B6": {
#           "content": "=-ODOO.BALANCE(ODOO.ACCOUNT.GROUP(\"income\"),$B$4)"
#         },
#         "B7": {
#           "content": "=ODOO.BALANCE(ODOO.ACCOUNT.GROUP(\"expense_direct_cost\"),$B$4)"
#         },
#         "B8": { "content": "=B6-B7" },
#         "B9": { "content": "365" },
#         "B10": { "content": "=ROUND(IFERROR(B5/B8*B9))" },
#         "B11": { "content": "=PIVOT.VALUE(7,\"price_subtotal\")" },
#         "C1": { "content": "=FORMAT.LARGE.NUMBER(B1)" },
#         "C2": { "content": "=FORMAT.LARGE.NUMBER(B2)" },
#         "C3": { "content": "=FORMAT.LARGE.NUMBER(B3)" },
#         "C10": {
#           "content": "=CONCATENATE(FORMAT.LARGE.NUMBER(B10),_t(\" days\"))"
#         },
#         "C11": { "content": "=FORMAT.LARGE.NUMBER(B11)" }
#       },
#       "styles": { "C1:C3": 6, "C10:C11": 6 },
#       "formats": { "B10": 1 },
#       "borders": {},
#       "conditionalFormats": [],
#       "figures": [],
#       "tables": [],
#       "areGridLinesVisible": true,
#       "isVisible": true,
#       "headerGroups": { "ROW": [], "COL": [] },
#       "dataValidationRules": [],
#       "comments": {}
#     }
#   ],
#   "styles": {
#     "1": { "textColor": "#01666b", "bold": true, "fontSize": 16 },
#     "2": { "textColor": "#434343", "bold": true, "fontSize": 11 },
#     "3": { "textColor": "#01666B", "verticalAlign": "middle" },
#     "4": { "textColor": "#434343", "verticalAlign": "middle" },
#     "5": {
#       "textColor": "#434343",
#       "bold": true,
#       "fontSize": 11,
#       "align": "center"
#     },
#     "6": { "fillColor": "#f8f9fa" }
#   },
#   "formats": { "1": "#,##0.00" },
#   "borders": {
#     "1": { "bottom": { "style": "thin", "color": "#CCCCCC" } },
#     "2": { "top": { "style": "thin", "color": "#CCCCCC" } },
#     "3": {
#       "bottom": { "style": "thick", "color": "#FFFFFF" },
#       "right": { "style": "thick", "color": "#FFFFFF" }
#     },
#     "4": {
#       "top": { "style": "thick", "color": "#FFFFFF" },
#       "bottom": { "style": "thick", "color": "#FFFFFF" },
#       "right": { "style": "thick", "color": "#FFFFFF" }
#     },
#     "5": { "top": { "style": "thick", "color": "#FFFFFF" } },
#     "6": {
#       "bottom": { "style": "thick", "color": "#FFFFFF" },
#       "left": { "style": "thick", "color": "#FFFFFF" },
#       "right": { "style": "thick", "color": "#FFFFFF" }
#     },
#     "7": {
#       "top": { "style": "thick", "color": "#FFFFFF" },
#       "bottom": { "style": "thick", "color": "#FFFFFF" },
#       "left": { "style": "thick", "color": "#FFFFFF" },
#       "right": { "style": "thick", "color": "#FFFFFF" }
#     },
#     "8": {
#       "bottom": { "style": "thick", "color": "#FFFFFF" },
#       "left": { "style": "thick", "color": "#FFFFFF" }
#     },
#     "9": {
#       "top": { "style": "thick", "color": "#FFFFFF" },
#       "bottom": { "style": "thick", "color": "#FFFFFF" },
#       "left": { "style": "thick", "color": "#FFFFFF" }
#     }
#   },
#   "revisionId": "START_REVISION",
#   "uniqueFigureIds": true,
#   "settings": {
#     "locale": {
#       "name": "English (US)",
#       "code": "en_US",
#       "thousandsSeparator": ",",
#       "decimalSeparator": ".",
#       "dateFormat": "mm/dd/yyyy",
#       "timeFormat": "hh:mm:ss",
#       "formulaArgSeparator": ",",
#       "weekStart": 7
#     }
#   },
#   "pivots": {
#     "1": {
#       "type": "ODOO",
#       "fieldMatching": {
#         "757a1b4b-e339-4879-beb6-9851050387cf": {
#           "chain": "invoice_date",
#           "type": "date",
#           "offset": 0
#         }
#       },
#       "context": { "group_by": ["invoice_date"] },
#       "domain": [
#         "&",
#         ["state", "not in", ["draft", "cancel"]],
#         "&",
#         ["product_categ_id", "!=", false],
#         ["price_subtotal", ">=", 0]
#       ],
#       "id": "1",
#       "measures": [
#         {
#           "id": "price_subtotal",
#           "fieldName": "price_subtotal"
#         }
#       ],
#       "model": "account.invoice.report",
#       "name": "Top Categories",
#       "sortedColumn": {
#         "groupId": [[], []],
#         "measure": "price_subtotal",
#         "order": "desc"
#       },
#       "formulaId": "1",
#       "columns": [],
#       "rows": [{ "fieldName": "product_categ_id" }]
#     },
#     "2": {
#       "type": "ODOO",
#       "fieldMatching": {
#         "757a1b4b-e339-4879-beb6-9851050387cf": {
#           "chain": "invoice_date",
#           "type": "date",
#           "offset": 0
#         }
#       },
#       "context": { "group_by": ["invoice_date"] },
#       "domain": [
#         "&",
#         ["state", "not in", ["draft", "cancel"]],
#         "&",
#         ["country_id", "!=", false],
#         ["price_subtotal", ">=", 0]
#       ],
#       "id": "2",
#       "measures": [
#         {
#           "id": "price_subtotal",
#           "fieldName": "price_subtotal"
#         }
#       ],
#       "model": "account.invoice.report",
#       "name": "Top Countries",
#       "sortedColumn": {
#         "groupId": [[], []],
#         "measure": "price_subtotal",
#         "order": "desc"
#       },
#       "formulaId": "2",
#       "columns": [],
#       "rows": [{ "fieldName": "country_id" }]
#     },
#     "3": {
#       "type": "ODOO",
#       "fieldMatching": {
#         "757a1b4b-e339-4879-beb6-9851050387cf": {
#           "chain": "invoice_date",
#           "type": "date",
#           "offset": 0
#         }
#       },
#       "context": { "group_by": ["invoice_date"] },
#       "domain": [
#         "&",
#         ["state", "not in", ["draft", "cancel"]],
#         "&",
#         ["product_id", "!=", false],
#         ["price_subtotal", ">=", 0]
#       ],
#       "id": "3",
#       "measures": [
#         {
#           "id": "price_subtotal",
#           "fieldName": "price_subtotal"
#         }
#       ],
#       "model": "account.invoice.report",
#       "name": "Top Products",
#       "sortedColumn": {
#         "groupId": [[], []],
#         "measure": "price_subtotal",
#         "order": "desc"
#       },
#       "formulaId": "3",
#       "columns": [],
#       "rows": [{ "fieldName": "product_id" }]
#     },
#     "4": {
#       "type": "ODOO",
#       "fieldMatching": {
#         "757a1b4b-e339-4879-beb6-9851050387cf": {
#           "chain": "invoice_date",
#           "type": "date",
#           "offset": 0
#         }
#       },
#       "context": { "group_by": ["invoice_date"] },
#       "domain": [
#         "&",
#         ["state", "not in", ["draft", "cancel"]],
#         "&",
#         ["invoice_user_id", "!=", false],
#         ["price_subtotal", ">=", 0]
#       ],
#       "id": "4",
#       "measures": [
#         {
#           "id": "price_subtotal",
#           "fieldName": "price_subtotal"
#         }
#       ],
#       "model": "account.invoice.report",
#       "name": "Top Salespeople",
#       "sortedColumn": {
#         "groupId": [[], []],
#         "measure": "price_subtotal",
#         "order": "desc"
#       },
#       "formulaId": "4",
#       "columns": [],
#       "rows": [{ "fieldName": "invoice_user_id" }]
#     },
#     "5": {
#       "type": "ODOO",
#       "fieldMatching": {
#         "757a1b4b-e339-4879-beb6-9851050387cf": {
#           "chain": "invoice_date",
#           "type": "date",
#           "offset": 0
#         }
#       },
#       "context": { "group_by": ["invoice_date"] },
#       "domain": [
#         "&",
#         ["state", "not in", ["draft", "cancel"]],
#         "|",
#         ["move_type", "=", "out_invoice"],
#         ["move_type", "=", "out_refund"]
#       ],
#       "id": "5",
#       "measures": [{ "id": "price_subtotal", "fieldName": "price_subtotal" }],
#       "model": "account.invoice.report",
#       "name": "KPI - Income",
#       "sortedColumn": null,
#       "formulaId": "5",
#       "columns": [],
#       "rows": []
#     },
#     "6": {
#       "type": "ODOO",
#       "fieldMatching": {
#         "757a1b4b-e339-4879-beb6-9851050387cf": {
#           "chain": "invoice_date",
#           "type": "date",
#           "offset": 0
#         }
#       },
#       "context": { "group_by": ["invoice_date"] },
#       "domain": [
#         "&",
#         ["state", "not in", ["draft", "cancel"]],
#         "|",
#         ["move_type", "=", "out_invoice"],
#         ["move_type", "=", "out_refund"]
#       ],
#       "id": "6",
#       "measures": [
#         { "id": "move_id", "fieldName": "move_id" },
#         { "id": "price_subtotal", "fieldName": "price_subtotal" }
#       ],
#       "model": "account.invoice.report",
#       "name": "KPI - Average Invoice",
#       "sortedColumn": null,
#       "formulaId": "6",
#       "columns": [],
#       "rows": []
#     },
#     "7": {
#       "type": "ODOO",
#       "fieldMatching": {
#         "757a1b4b-e339-4879-beb6-9851050387cf": {
#           "chain": "invoice_date",
#           "type": "date",
#           "offset": 0
#         },
#
#         "accd0cbe-12c9-4cab-93a1-afa5080dd635": {
#           "chain": "product_id",
#           "type": "many2one"
#         },
#         "02acc7f7-b282-4ce9-bf38-6abfb72be6aa": {
#           "chain": "invoice_user_id",
#           "type": "many2one"
#         }
#       },
#       "context": { "group_by": ["invoice_date"] },
#       "domain": [
#         "&",
#         ["state", "not in", ["draft", "cancel"]],
#         "&",
#         "|",
#         ["move_type", "=", "out_invoice"],
#         ["move_type", "=", "out_refund"],
#         ["payment_state", "=", "not_paid"]
#       ],
#       "id": "7",
#       "measures": [{ "id": "price_subtotal", "fieldName": "price_subtotal" }],
#       "model": "account.invoice.report",
#       "name": "KPI - Unpaid Invoices",
#       "sortedColumn": null,
#       "formulaId": "7",
#       "columns": [],
#       "rows": []
#     }
#   },
#   "pivotNextId": 8,
#   "customTableStyles": {},
#   "odooVersion": 12,
#   "globalFilters": [
#     {
#       "id": "757a1b4b-e339-4879-beb6-9851050387cf",
#       "type": "date",
#       "label": "Period",
#       "defaultValue": "last_three_months",
#       "rangeType": "relative"
#     }
#   ],
#   "lists": {
#     "1": {
#       "columns": [
#         "name",
#         "invoice_partner_display_name",
#         "invoice_date",
#         "invoice_date_due",
#         "activity_ids",
#         "amount_untaxed_signed",
#         "amount_total_signed",
#         "amount_total_in_currency_signed",
#         "payment_state",
#         "state"
#       ],
#       "domain": [
#         "&",
#         ["state", "not in", ["draft", "cancel"]],
#         ["move_type", "=", "out_invoice"]
#       ],
#       "model": "account.move",
#       "context": { "default_move_type": "out_invoice" },
#       "orderBy": [{ "name": "amount_total_signed", "asc": false }],
#       "id": "1",
#       "name": "Invoices by Total Signed",
#       "fieldMatching": {
#         "757a1b4b-e339-4879-beb6-9851050387cf": {
#           "chain": "date",
#           "type": "date",
#           "offset": 0
#         }
#       }
#     }
#   },
#   "listNextId": 2,
#   "chartOdooMenusReferences": {
#     "5ea5dd7f-9f83-4482-a2bb-2ec72ab35912": "account.menu_finance",
#     "1aeea7b2-900b-4067-b8ad-3e4772c54028": "account.menu_action_move_out_invoice_type",
#     "bdfb27d0-5902-4a2a-9b7e-514a6625578c": "account.menu_action_account_invoice_report_all",
#     "b1673523-d139-47fb-b5ea-9e4f969aacb6": "account.menu_action_account_invoice_report_all"
#   }
# }