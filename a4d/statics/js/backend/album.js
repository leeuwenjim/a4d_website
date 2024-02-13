
document.addEventListener("DOMContentLoaded", function(event) {
    show_albums();
});

var busy = false;
var modal_showing = false;

function show_albums() {
    if (busy) return;
    busy = true;
    console.log('hmmm')
    $('#album_view').html('');

    $.get('/api/albums/', {}, (data) => {
        $table = $('<table>').css('width', '100%');

        $table.append(
            $('<thead>').append(
                $('<tr>').append(
                    $('<th>').css('text-align', 'left').text('Albums'),
                    $('<th>').css('width', '100px').html('&nbsp;'),
                    $('<th>').css('width', '100px').html('&nbsp;'),
                    $('<th>').css('width', '100px').html('&nbsp;'),
                )
            )
        )

        $table_body = $('<tbody>')

        var years = Object.keys(data.data).sort().reverse();

        years.forEach((year) => {
            $table_body.append(
                $('<tr>').append(
                    $('<th>', {'colspan': 4}).css('text-align', 'left').text(year.toString())
                )
            );
            data.data[year].forEach((album) => {
                $table_body.append(
                    $('<tr>').append(
                        $('<td>').text(album.title),
                        $('<td>').append(
                            $('<button>', {'class': 'add_button'}).text('Bekijk').on('click', () => {
                                window.location.href = '/beheer/album/' + album.slug + '/';
                            })
                        ),
                        $('<td>').append(
                            $('<button>', {'class': 'edit_button'}).text('Bewerk').on('click', () => {
                                edit_album(album.id, album.title, year);
                            })
                        ),
                        $('<td>').append(
                            $('<button>', {'class': 'delete_button'}).text('Verwijder').on('click', () => {
                                delete_album(album.id);
                            })
                        )
                    )
                )
            })
        });

        $table.append($table_body);
        $('#album_view').html('');
        $('#album_view').append($table);
        busy = false;
    }).fail(function (xhr, status, error) {
        fail_message($('#error_container'), xhr);
        busy = false;
    });
}

function add_album() {
    if (busy) return;
    busy = true;
    $('#add_button').attr('disabled', true);
    $.post('/api/albums/', {
        'title': $('#input_title').val(),
        'year': $('#input_year').val(),
    }, (data) => {
        create_message($('#error_container'), 'success', 'Album toegevoegd', 'Het album is goed aangemaakt en er kunnen nu afbeeldingen binnen toegevoegd worden.');
        $('#input_title').val('');
        $('#input_year').val(new Date().getFullYear().toString());
        $('#add_button').attr('disabled', false)
        busy = false;
        show_albums();
    }).fail(function (xhr, status, error) {
        busy = false;
        fail_message($('#error_container'), xhr);
        $('#add_button').attr('disabled', false);
    })
}

function edit_album(album_id, title, year) {
    if (busy) return;
    if (modal_showing) return;

    modal_showing = true;
    busy = true;

    modal_showing = true;
    new Modal({
        'modal': $('#album_edit_modal'),
        'onShow': (modal_object) => {
            $('#edit_input_title').val(title);
            $('#edit_input_year').val(year);
        },
        'onAccept': (modal_object) => {
            modal_object.disable_buttons();
            const send_data = {
                'title': $('#edit_input_title').val(),
                'year': $('#edit_input_year').val(),
            };

            $.put('/api/albums/' + album_id.toString() + '/', send_data, (data) => {
                modal_object.enable_buttons();
                modal_object.close();
                show_albums();
            }).fail(function (xhr, status, error) {
                modal_object.enable_buttons();
                fail_message($('#modal_error_container'), xhr);
            });

            return false;
        },
        'onHide': () => {
            $('#edit_input_year').val('');
            $('#edit_input_title').val('');
            modal_showing = false;
            busy = false;
        },
    }).show();


}

function delete_album(album_id) {
    if (busy) return;
    if (!confirm('Weet u zeker dat u het album wilt verwijderen?')) return;
    busy = true;
    $.delete('/api/albums/' + album_id.toString() + '/', (data) => {
        busy = false;
        create_message($('#album_view'), 'success', 'Album verwijderd', 'Het album en alle bijbehorende foto\'s zijn verwijderd.');
        show_albums();
    }).fail(function (xhr, error, status) {
        busy = false;
        fail_message($('#album_view'), xhr);
    })
}