from odoo import models
from odoo.http import request


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        res = super(Http, self).session_info()
        user = request.env.user

        # Add branch data
        res.update({
            "user_branches": {
                "financial_year": (user.financial_year_id.id, user.financial_year_id.name) if user.financial_year_id else (None, ''),
                "allowed_financial_year": [(b.id, b.name) for b in user.allowed_financial_year_id]
            }
        })
        return res

# {
#   "version": 21,
#   "sheets": [
#     {
#       "id": "a7cd7db1-9407-4895-82f2-7657102c7688",
#       "name": "Dashboard",
#       "colNumber": 7,
#       "rowNumber": 69,
#       "rows": { "6": { "size": 40 }, "22": { "size": 40 } },
#       "cols": {
#         "0": { "size": 225 }, "1": { "size": 150 }, "2": { "size": 100 },
#         "3": { "size": 50 }, "4": { "size": 225 }, "5": { "size": 150 }, "6": { "size": 100 }
#       },
#       "cells": {
#         "A7": {
#           "content": "[Invoiced by Month](odoo://view/{\"viewType\":\"graph\",\"action\":{\"domain\":[\"&\",[\"state\",\"not in\",[\"draft\",\"cancel\"]],\"|\",[\"move_type\",\"=\",\"out_invoice\"],[\"move_type\",\"=\",\"out_refund\"]],\"context\":{\"group_by\":[\"invoice_date\"],\"graph_measure\":\"price_subtotal\",\"graph_mode\":\"line\",\"graph_groupbys\":[\"invoice_date:month\"]},\"modelName\":\"account.invoice.report\",\"views\":[[false,\"graph\"],[false,\"pivot\"],[false,\"search\"]]},\"threshold\":0,\"name\":\"Invoices Analysis\",\"positional\":true})"
#         }
#       },
#       "styles": { "A7": 1 },
#       "borders": { "A7:G7": 1 },
#       "figures": [
#         {
#           "id": "5ea5dd7f-9f83-4482-a2bb-2ec72ab35912",
#           "x": 0, "y": 178, "width": 1000, "height": 345, "tag": "chart",
#           "data": {
#             "title": { "text": "" },
#             "background": "#FFFFFF",
#             "legendPosition": "none",
#             "metaData": { "groupBy": ["invoice_date:month"], "measure": "price_subtotal", "order": null, "resModel": "account.invoice.report", "mode": "line" },
#             "searchParams": {
#               "comparison": null,
#               "context": { "group_by": ["invoice_date"] },
#               "domain": ["&", ["state", "not in", ["draft", "cancel"]], "|", ["move_type", "=", "out_invoice"], ["move_type", "=", "out_refund"]],
#               "groupBy": ["invoice_date"],
#               "orderBy": []
#             },
#             "type": "odoo_line",
#             "verticalAxisPosition": "left",
#             "stacked": false,
#             "fillArea": true,
#             "fieldMatching": { "757a1b4b-e339-4879-beb6-9851050387cf": { "chain": "invoice_date", "type": "date", "offset": 0 } }
#           }
#         },
#         {
#           "id": "1aeea7b2-900b-4067-b8ad-3e4772c54028",
#           "x": 0, "y": 11, "width": 200, "height": 109, "tag": "chart",
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
#         }
#       ],
#       "areGridLinesVisible": true
#     },
#     {
#       "id": "685cb5c3-4acb-45eb-8000-99e1af15b3ed",
#       "name": "Data",
#       "colNumber": 26,
#       "rowNumber": 107,
#       "cells": {
#         "A1": { "content": "=_t(\"KPI - Invoice Count\")" },
#         "B1": { "content": "=PIVOT.VALUE(5,\"move_id\")" },
#         "C1": { "content": "=FORMAT.LARGE.NUMBER(B1)" }
#       }
#     }
#   ],
#   "pivots": {
#     "5": {
#       "type": "ODOO",
#       "fieldMatching": {
#         "757a1b4b-e339-4879-beb6-9851050387cf": { "chain": "invoice_date", "type": "date", "offset": 0 }
#       },
#       "context": { "group_by": ["invoice_date"] },
#       "domain": [
#         "&", ["state", "not in", ["draft", "cancel"]],
#         "|", ["move_type", "=", "out_invoice"], ["move_type", "=", "out_refund"]
#       ],
#       "id": "5",
#       "measures": [
#         { "id": "move_id", "fieldName": "move_id" }
#       ],
#       "model": "account.invoice.report",
#       "name": "KPI - Invoice Count",
#       "formulaId": "5",
#       "columns": [],
#       "rows": []
#     }
#   }
# }