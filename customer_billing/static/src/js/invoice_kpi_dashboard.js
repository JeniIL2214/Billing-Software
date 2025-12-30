// static/src/js/invoice_kpi_dashboard.js
odoo.define('invoice_kpi_dashboard_inherit', function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;

    var InvoiceKPIDashboard = AbstractAction.extend({
        template: 'InvoiceKPIDashboardTemplate',
        init: function (parent, action) {
            this._super(parent, action);
        },
        start: function () {
            var self = this;
            return this._fetch_and_render();
        },
        _fetch_and_render: function () {
            var self = this;
            return rpc.query({
                route: '/invoice_kpi_dashboard/data',
                params: {}
            }).then(function (result) {
                // render template with result
                self.$el.html(QWeb.render('InvoiceKPIDashboardTemplate', {kpis: result}));

                // Format numbers (simple)
                self.$('.kpi-number').each(function () {
                    var v = $(this).data('value');
                    if (v === undefined || v === null) {
                        $(this).text('-');
                    } else {
                        // display two decimals for amounts, integer for counts/dso
                        var kind = $(this).data('kind');
                        if (kind === 'amount') {
                            $(this).text(Number(v).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
                        } else {
                            $(this).text(Number(v).toLocaleString());
                        }
                    }
                });

                // add click handlers: navigate to invoice list filtered for out_invoice
                self.$('#open_invoices_action').off('click').on('click', function () {
                    var domain = [['move_type', '=', 'out_invoice'], ['state', 'not in', ['draft', 'cancel']]];
                    self.do_action({
                        type: 'ir.actions.act_window',
                        name: 'Customer Invoices',
                        res_model: 'account.move',
                        views: [[false, 'list'], [false, 'form']],
                        domain: domain,
                    });
                });
            });
        },
    });

    core.action_registry.add('invoice_kpi_dashboard', InvoiceKPIDashboard);
    return InvoiceKPIDashboard;
});
