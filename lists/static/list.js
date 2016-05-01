/*global $ */

window.Superlists = window.Superlists || {};
window.Superlists.Lists = {

    initialize: function (options) {
        $('input').on('keypress', function () {
            $('.has-error').hide();
        });

        if (options && options.listItemsUrl) {
            url = options.listItemsUrl;
            $('#id_item_form').on('submit', function(event) {
                event.preventDefault();
                window.Superlists.Lists.postItem(options.listItemsUrl);
            });
            window.Superlists.Lists.getItems(options.listItemsUrl);
        }
    },

    getItems: function (url) {
        $.get(url).success(function (response) {
            var rows = '';
            for (var i=0; i<response.length; i++) {
                var item = response[i];
                rows += '\n<tr><td>' + (i+1) + ': ' + item.text + '</td></tr>';
            }
            $('#id_list_table').html(rows);
        });
    },

    postItem: function (url) {
        var form = $('#id_item_form');
        $.post(url, {
            'text': form.find('input[name="text"]').val(),
            'csrfmiddlewaretoken': form.find('input[name="csrfmiddlewaretoken"]').val(),
        }).success(function () {
            window.Superlists.Lists.getItems(url);
            $('.has-error').hide();
        }).error(function (xhr) {
            $('.has-error').show();
            $('.has-error .help-block').text(JSON.parse(xhr.responseText).error);
        });
    }
};
