var busy = false;

document.addEventListener("DOMContentLoaded", function(event) {
    show_data();
});

function show_data() {
    if (busy) {
        return;
    }
    busy = true;

    $.get('/api/thanx/', {}, (data) => {
        $thanx_data = $('#thanx_data');
        $thanx_data.html('');

        data.forEach(item => {
            $thanx_data.append(
                $('<tr>').append(
                    $('<td>').append(
                        $('<input>', {
                            'id': 'input_' + item.id.toString(),
                            'placeholder': 'Nieuwe naam...',
                            'type': 'text',
                            'max_length': '40',
                            'value': item.name,
                            'style': 'width: 100%',
                        })
                    ),
                    $('<td>').append(
                        $('<button>', {'id': 'edit_button', 'class': 'edit_button'}).text('Bewerk').on('click', () => {
                            edit_thanks(item.id.toString());
                        })
                    ),
                    $('<td>').append(
                        $('<button>', {'id': 'delete_button', 'class': 'delete_button'}).text('Verwijder').on('click', () => {
                            delete_thanx(item.id.toString());
                        })
                    ),
                )
            )
        })

        $thanx_data.append(
            $('<td>').append(
                $('<input>', {
                    'id': 'input_new',
                    'placeholder': 'Nieuw...',
                    'type': 'text',
                    'max_length': '40',
                    'style': 'width: 100%',
                })
            ),
            $('<td>', {'colspan': '2'}).append(
                $('<button>', {'id': 'add_button', 'class': 'add_button', 'style': 'width: 100%'}).text('Voeg toe').on('click', () => {
                    add_thanx()
                })
            )
        )
        busy = false;
    }).fail(function (xhr, status, error) {
        busy = false;
        fail_message($('#error_container'), xhr);
    });
}

function add_thanx() {
    if (busy) {
        return;
    }
    busy = true;
    $.post('/api/thanx/', {'name': $('#input_new').val()}, (data) => {
        busy = false;
        show_data();
    }).fail(function (xhr, status, error) {
        busy = false;
        fail_message($('#error_container'), xhr);
    });
}

function edit_thanks(tid) {
    if (busy) {
        return;
    }
    busy = true;
    $.put('/api/thanx/' + tid + '/', {'name': $('#input_' + tid).val()}, (data) => {
        busy = false;
        show_data();
    }).fail(function (xhr, status, error) {
        busy = false;
        fail_message($('#error_container'), xhr);
    });
}

function delete_thanx(tid) {
    if (busy) return;
    busy = true;
    if (!confirm('Weet u zeker dat u het album wilt verwijderen?')) return;
    $.delete('/api/thanx/' + tid + '/', {}, (data) => {
        busy = false;
        show_data();
    }).fail(function (xhr, status, error) {
        busy = false;
        fail_message($('#error_container'), xhr);
    });
}
