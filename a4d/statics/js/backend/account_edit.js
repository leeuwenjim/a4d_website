function edit_account(account_id) {

    $('#edit_button').attr('disabled', true);

    $.put('/api/users/' + account_id.toString() + '/', {
        'first_name': $('#edit_input_first_name').val(),
        'last_name': $('#edit_input_last_name').val(),
        'username': $('#edit_input_username').val(),
    }, (data) => {
        create_message($('#error_container'), 'success', 'Gegevens zijn aangepast', 'Uw doorgegeven veranderingen zijn succesvol opgeslagen.')
    }).fail(function (xhr, status, error) {
        fail_message($('#error_container'), xhr);
    });

    $('#edit_button').attr('disabled', false);

}
