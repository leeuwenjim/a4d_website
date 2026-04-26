var modal_showing = false;
var busy = false;


document.addEventListener("DOMContentLoaded", function(event) {
    show_sponsor_data();
});

function show_sponsor_data() {
    if (busy) {
        return;
    }
    busy = true;

    $.get('/api/sponsors/', {}, (data) => {
        $thanx_data = $('#sponsor_data');
        $thanx_data.html('');

        data.forEach(item => {
            $thanx_data.append(
                $('<tr>', {'id': 'sponsor_row_' + item.id.toString()}).append(
                    $('<td>').text(item.name),
                    $('<td>').append(
                        $('<button>', {'id': 'edit_button', 'class': 'edit_button'}).text('Bewerk').on('click', () => {
                            edit_sponsor(item.id.toString());
                        })
                    ),
                    $('<td>').append(
                        $('<button>', {'id': 'delete_button', 'class': 'delete_button'}).text('Verwijder').on('click', () => {
                            delete_sponsor(item.id.toString());
                        })
                    ),
                ),
            )
        });

        busy = false;
    }).fail(function (xhr, status, error) {
        busy = false;
        fail_message($('#error_container'), xhr);
    });
}


function create_sponsor_item() {
    if (busy) return;
    busy = true;

    const send_data = {
        'name': $('#input_title').val(),
        'content': $('#input_content').val(),
    };

    $.post('/api/sponsors/', send_data, (data) => {
        $('#input_title').val('');
        $('#input_content').val('');
        
        console.log(data);
        show_sponsor_data();

        create_message($('#error_container'), 'success', 'Sponsor aangemaakt', 'Het bericht is succesvol opgeslagen.')
        busy = false;
    }).fail(function (xhr, status, error) {
        fail_message($('#error_container'), xhr);
        busy = false;
    });
}

function delete_sponsor(tid) {
    if (busy) return;
    busy = true;
    if (!confirm('Weet u zeker dat u het album wilt verwijderen?')) return;
    $.delete('/api/sponsors/' + tid + '/', {}, (data) => {
        busy = false;
        $('#sponsor_row_' + tid).remove();
    }).fail(function (xhr, status, error) {
        busy = false;
        fail_message($('#error_container'), xhr);
    });
}

function upload_extra(sponsor_id, modal_object, failed)
{
    
    const $file_input = $('#input_extra')[0];
    const selected_files = $file_input.files;
    var this_failed = failed;

    if (selected_files.length > 0)
    {
        const send_data = new FormData();
            send_data.append('extra', selected_files[0], selected_files[0].name);

            $.ajax({
                type: 'POST',
                url: '/api/sponsors/'+ sponsor_id.toString() +'/extra/',
                success: function (data) {
                },
                error: function (xhr, status, error) {
                    create_message($('#modal_error_container'), 'error', "Kon Extra niet uploaded", "Helaas is er met het extra opslaan iets mis gegaan. Code: " + xhr.status);
                },
                async: true,
                data: send_data,
                cache: false,
                contentType: false,
                processData: false,
                timeout: 60000,
            })
    }
    else {
        console.log("No extra file: " + sponsor_id);
    }


    modal_object.enable_buttons();
    if (this_failed == false)
    {
        modal_object.close();
        show_sponsor_data();
    }
}

function upload_logo(sponsor_id, modal_object, failed)
{
    const $file_input = $('#input_logo')[0];
    const selected_files = $file_input.files;

    if (selected_files.length > 0)
    {
        const send_data = new FormData();
            send_data.append('logo', selected_files[0], selected_files[0].name);

            $.ajax({
                type: 'POST',
                url: '/api/sponsors/'+ sponsor_id.toString() +'/logo/',
                success: function (data) {
                    
                     upload_extra(sponsor_id, modal_object, failed);
                },
                error: function (xhr, status, error) {
                    create_message($('#modal_error_container'), 'error', "Kon Logo niet uploaded", "Helaas is er met het logo opslaan iets mis gegaan. Code: " + xhr.status);
                     upload_extra(sponsor_id, modal_object, true);
                },
                async: true,
                data: send_data,
                cache: false,
                contentType: false,
                processData: false,
                timeout: 60000,
            })
    }
    else {
        console.log("No file: " + sponsor_id);
        upload_extra(sponsor_id, modal_object, failed);
    }
}

function upload_data(sponsor_id, modal_object)
{
    const send_data = {
        'name': $('#input_edit_title').val(),
        'content': $('#input_edit_content').val(),
    };

    console.log("Called for: " + sponsor_id);
    $.put('/api/sponsors/' + sponsor_id.toString() + '/', send_data, (data) => {
        upload_logo(sponsor_id, modal_object, false);
    }).fail(function (xhr, status, error) {
        fail_message($('#modal_error_container'), xhr);
        upload_logo(sponsor_id, modal_object, true);
    });

}

function edit_sponsor(item_id) {
    if (modal_showing) return;
    modal_showing = true;
    new Modal({
        'modal': $('#sponsor_edit_modal'),
        'onShow': (modal_object) => {
            $.get('/api/sponsors/' + item_id.toString() + '/', {}, (data) => {
                $('#input_edit_title').val(data.name);
                $('#input_edit_content').val(data.content);
                $('#current_logo').text(data.logo_url);
                if (data.logo_url)
                {
                    $("#delete_logo").show();
                    $("#delete_logo").off('click').on('click', () =>{
                        delete_logo(item_id);
                    });

                }
                else 
                {
                    $("#delete_logo").hide();
                }
                $('#current_extra').text(data.extra_url);
                if (data.extra_url)
                {
                    $("#delete_extra").show();
                    $("#delete_extra").off('click').on('click', () =>{
                        delete_extra(item_id);
                    });

                }
                else 
                {
                    $("#delete_extra").hide();
                }
            }).fail(function (xhr, status, error) {
                modal_object.disable_buttons();
                fail_message($('#modal_error_container'), xhr);
            });
        },
        'onAccept': (modal_object) => {
            modal_object.disable_buttons();
            upload_data(item_id, modal_object);
            return false;
        },
        'onHide': (modal_object) => {
            $('#input_edit_title').val('');
            $('#input_edit_content').val('');
            $('#input_logo').val("");
            $('#input_extra').val("");
            $('#current_logo').text("");
            $('#current_extra').text("");
            modal_object.enable_buttons();
            modal_showing = false;
        },
    }).show();
}

function delete_logo(sponsor_id) {
    if (busy) return;
    busy = true;
    if (!confirm('Weet u zeker dat u het logo wilt verwijderen?')) return;
    $.delete('/api/sponsors/' + sponsor_id + '/logo/', {}, (data) => {
        busy = false;
            $('#current_logo').text("");
        create_message($('#modal_error_container'), 'success', 'Logo verwijderd', 'Logo is verwijderd.');
    }).fail(function (xhr, status, error) {
        busy = false;
        fail_message($('#modal_error_container'), xhr);
    });
}

function delete_extra(sponsor_id) {
    if (busy) return;
    busy = true;
    if (!confirm('Weet u zeker dat u de extra afbeelding wilt verwijderen?')) return;
    $.delete('/api/sponsors/' + sponsor_id + '/extra/', {}, (data) => {
        busy = false;
            $('#current_extra').text("");
        create_message($('#modal_error_container'), 'success', 'Extra afbeelding verwijderd', 'Extra afbeelding is verwijderd.');
    }).fail(function (xhr, status, error) {
        busy = false;
        fail_message($('#modal_error_container'), xhr);
    });
}
