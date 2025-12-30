console.log("✅ JS loaded: switch_financial_year_menu.js");

odoo.define('your_module.SwitchFinancialYearMenu', function(require) {
    "use strict";

    var config = require('web.config');
    var core = require('web.core');
    var session = require('web.session');
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var _t = core._t;

    var SwitchFinancialYearMenu = Widget.extend({
        template: 'SwitchFinancialYearMenu',

        willStart: function() {
            console.log("🕐 willStart: Checking session.user_branches...");
            this.isMobile = config.device.isMobile;
            if (!session.user_branches) {
                console.warn("⚠️ No user_branches found in session.");
                return $.Deferred().reject();
            }
            return this._super();
        },

        start: function() {
            console.log("🚀 start: Initializing dropdown menu");
            var self = this;
            var financial_year = session.user_branches.financial_year;
            var allowed_financial_year = session.user_branches.allowed_financial_year;

            this.$el.on('click', '.dropdown-menu li a[data-menu]', _.debounce(function(ev) {
                ev.preventDefault();
                var financial_year_id = $(ev.currentTarget).data('financial-year-id');
                console.log("📥 Selected FY ID:", financial_year_id);

                self._rpc({
                    model: 'res.users',
                    method: 'write',
                    args: [[session.uid], { 'financial_year_id': financial_year_id }],
                }).then(function() {
                    console.log("✅ FY updated. Reloading page...");
                    location.reload();
                });
            }, 1500, true));

            if ((!financial_year || !financial_year[0]) && allowed_financial_year.length === 1) {
                var auto_financial_year_id = allowed_financial_year[0][0];
                console.log("ℹ️ Auto-selecting only FY:", auto_financial_year_id);

                this._rpc({
                    model: 'res.users',
                    method: 'write',
                    args: [[session.uid], { 'financial_year_id': auto_financial_year_id }],
                }).then(function() {
                    location.reload();
                });
                return;
            }

            let dropdown_html = '';
            if (this.isMobile) {
                dropdown_html = '<li class="bg-info">' + _t('Tap on the list to change FY') + '</li>';
            }

            if (financial_year && financial_year[1]) {
                self.$('.oe_topbar_name').text(financial_year[1]);
            } else {
                self.$('.oe_topbar_name').text("Select FY");
                self.do_notify(_t("No Financial Year Selected"), _t("Please select a FY from the dropdown."));
            }

            _.each(allowed_financial_year, function(fy) {
                var prefix = (fy[0] === (financial_year && financial_year[0])) ?
                    '<i class="fa fa-check mr8"></i>' :
                    '<span class="mr24"/>';
                dropdown_html += '<li><a href="#" data-menu="FY" data-financial-year-id="' + fy[0] + '">' + prefix + fy[1] + '</a></li>';
            });

            self.$('.dropdown-menu').html(dropdown_html);
            return this._super();
        },
    });

    SystrayMenu.Items.push(SwitchFinancialYearMenu);
    return SwitchFinancialYearMenu;
});
