var busy = false;
var modal_showing = false;

document.addEventListener("DOMContentLoaded", function(event) {
    get_all_users();
});

function get_all_users() {
    if (busy) return;
    busy = true;

    $.get('/api/users/', {}, (data) => {
        var $user_data = $('#user_data');
        $user_data.html('');

        data.forEach((user) => {
            $user_data.append(
                $('<tr>').append(
                    $('<td>').text(user.first_name + ' ' + user.last_name),
                    $('<td>').append(
                        $('<button>', {'id': 'edit_button', 'class': 'edit_button'}).text('Reset').on('click', () => {
                            reset_password(user.id.toString(), user.username);
                        })
                    ),
                    $('<td>').append(
                        $('<button>', {
                            'id': 'delete_button',
                            'class': 'delete_button'
                        }).text('Verwijder').on('click', () => {
                            delete_user(user.id.toString());
                        })
                    )
                )
            )
        });
        busy = false;
    }).fail(function (xhr, status, error) {
        busy = false;
        fail_message($('#top_message_container'), xhr);
    })

}

function reset_password(user_id, username) {
    if (modal_showing) return;
    modal_showing = true;
    new Modal({
        'modal': $('#item_edit_modal'),
        'onShow': (modal_object) => {
            $('#modal_username_field').text(username);
        },
        'onAccept': (modal_object) => {
            modal_object.disable_buttons();
            const send_data = {
                'ww1': $('#reset_input_ww1').val(),
                'ww2': $('#reset_input_ww2').val(),
            };

            $.put('/api/users/' + user_id + '/', send_data, (data) => {
                modal_object.enable_buttons();
                modal_object.close();
                create_message($('#top_message_container'), 'success', 'Wachtwoord aangepast', 'Het is gelukt om het wachtwoord successvol aan te passen.')
            }).fail(function (xhr, status, error) {
                modal_object.enable_buttons();
                fail_message($('#modal_error_container'), xhr);
            });

            return false;
        },
        'onHide': () => {
            $('#reset_input_ww1').val('');
            $('#reset_input_ww2').val('');
            modal_showing = false;
        },
    }).show();
}

function add_user() {
    if (busy) return;
    busy = true;
    const new_user_data = {
        'first_name': $('#input_first_name').val(),
        'last_name': $('#input_last_name').val(),
        'username': $('#input_username').val(),
        'ww1': $('#input_ww1').val(),
        'ww2': $('#input_ww2').val(),
    }
    $.post('/api/users/', new_user_data, (data) => {
        $('#input_first_name').val('');
        $('#input_last_name').val('');
        $('#input_username').val('');
        $('#input_ww1').val('');
        $('#input_ww2').val('');
        get_all_users();
    }).fail(function (xhr, status, error) {
        busy = false;
        fail_message($('#error_container'), xhr);
    });
}

function delete_user(user_id) {
    if (busy) return;
    if (!confirm('Weet u zeker dat u de beheerder wilt verwijderen?')) return;
    busy = true
    $.delete('/api/users/' + user_id + '/', {}, (data) => {
        get_all_users();
    }).fail(function (xhr, status, error) {
        busy = false;
        fail_message($('#error_container'), xhr);
    });
}