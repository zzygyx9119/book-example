/*global $ */

var initialize = function() {
    $('input').on('keypress', function () {
        $('.has-error').hide();
    });
};


window.Superlists = window.Superlists || {};
window.Superlists.Lists = window.Superlists.Lists || {
    initialize: initialize
};

