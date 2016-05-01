/*global $ */

var exports = {};

exports.initialize = function (options) {
    $('input').on('keypress', function () {
        $('.has-error').hide();
    });

    if (options && options.listItemsUrl) {
        url = options.listItemsUrl;
        $('#id_item_form').on('submit', function(event) {
            event.preventDefault();
            exports.postItem(options.listItemsUrl);
        });
        exports.getItems(options.listItemsUrl);
    }
};

exports.getItems = function (url) {
    $.get(url).success(function (response) {
        var rows = '';
        for (var i=0; i<response.length; i++) {
            var item = response[i];
            rows += '\n<tr><td>' + (i+1) + ': ' + item.text + '</td></tr>';
        }
        $('#id_list_table').html(rows);
    });
};

exports.postItem = function (url) {
    var form = $('#id_item_form');
    $.post(url, {
        'text': form.find('input[name="text"]').val(),
        'csrfmiddlewaretoken': form.find('input[name="csrfmiddlewaretoken"]').val(),
    }).success(function () {
        exports.getItems(url);
        $('.has-error').hide();
    }).error(function (xhr) {
        $('.has-error').show();
        $('.has-error .help-block').text(JSON.parse(xhr.responseText).error);
    });
};

window.Superlists = window.Superlists || {};
window.Superlists.Lists = exports;
