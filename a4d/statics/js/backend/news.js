var modal_showing = false;
var busy = false;
var pagination = null;

document.addEventListener("DOMContentLoaded", function(event) {
    pagination = new NewsControllPagination('/api/news/', $('#news_items'), $('#news_pagination_navigation'));
    pagination.load_page(1);
});


function edit_item(item_id) {
    if (modal_showing) return;
    modal_showing = true;
    new Modal({
        'modal': $('#item_edit_modal'),
        'onShow': (modal_object) => {
            $.get('/api/news/' + item_id.toString() + '/', {}, (data) => {
                $('#input_edit_title').val(data.title);
                $('#input_edit_content').val(data.content);
                $('#input_edit_link').val(data.link);
            }).fail(function (xhr, status, error) {
                modal_object.disable_buttons();
                fail_message($('#modal_error_container'), xhr);
            });
        },
        'onAccept': (modal_object) => {
            modal_object.disable_buttons();
            const send_data = {
                'title': $('#input_edit_title').val(),
                'content': $('#input_edit_content').val(),
                'link': $('#input_edit_link').val(),
            };

            $.put('/api/news/' + item_id.toString() + '/', send_data, (data) => {
                modal_object.enable_buttons();
                modal_object.close();
                pagination.load_page(pagination.current_page);
            }).fail(function (xhr, status, error) {
                modal_object.enable_buttons();
                fail_message($('#modal_error_container'), xhr);
            });

            return false;
        },
        'onHide': (modal_object) => {
            $('#input_edit_title').val('');
            $('#input_edit_content').val('');
            $('#input_edit_link').val('');
            modal_object.enable_buttons();
            modal_showing = false;
        },
    }).show();
}

function create_news_item() {
    if (busy) return;
    busy = true;

    const send_data = {
        'title': $('#input_title').val(),
        'content': $('#input_content').val(),
        'link': $('#input_link').val(),
    };

    $.post('/api/news/', send_data, (data) => {
        $('#input_title').val('');
        $('#input_content').val('');
        $('#input_link').val('');
        pagination.load_page(1);
        create_message($('#error_container'), 'success', 'Bericht aangemaakt', 'Het bericht is succesvol opgeslagen.')
        busy = false;
    }).fail(function (xhr, status, error) {
        fail_message($('#error_container'), xhr);
    });
}

function delete_news_item(item_id) {
    if (busy) return;
    if (!confirm('Weet u zeker dat u het nieuws item wilt verwijderen?')) return;
    busy = true;
    $.delete('/api/news/' + item_id.toString() + '/', {}, (data) => {
        pagination.load_page(pagination.current_page);
        busy = false;
    }).fail(function (xhr, status, error) {
        fail_message($('#error_container'), xhr);
    });
}