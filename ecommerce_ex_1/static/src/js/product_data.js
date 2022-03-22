odoo.define('ecommerce_ex_1.product_data', function (require) {
    "use strict";
    var ajax = require('web.ajax');
    const publicWidget = require('web.public.widget');

   publicWidget.registry.myCustomWidget = publicWidget.Widget.extend({
        selector: ".container",
        events: {
            'click .show_product': 'showProduct',
        },
        showProduct: function () {
            console.log("Done");
           ajax.jsonRpc("/product_page", 'call', {}).then(function (data) {
             $(".product_div").html(data);
           });
        },
    });
});


