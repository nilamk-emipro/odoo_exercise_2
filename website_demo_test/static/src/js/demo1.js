
odoo.define('website_demo_test.demo', function (require) {
var Widget = require('web.Widget');
var Counter = Widget.extend({
    template: 'some.template',
    events: {
        'click button': '_onClick',
    },
    init: function (parent, value) {
        this._super(parent);
        this.count = value;
    },
    _onClick: function () {
        this.count++;
        this.$('.val').text(this.count);
    },
});
});

