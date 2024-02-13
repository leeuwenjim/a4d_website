
var busy = false;
var album_id = '0';

document.addEventListener("DOMContentLoaded", function(event) {
    album_id = document.getElementById('album_id').textContent;
    //album_id = document.getElementById("id").src.split("id=")[1]
    show_images();
});

function show_images() {
    if (busy) return;
    busy = true;
    $.get('/api/albums/'+ album_id +'/images/', (data) => {
        $container = $('#picture_container');

        $container.html('');

        data.photos.forEach((photo) => {

            $container.append(
                $('<div>', {'class': 'img-card'}).append(
                    $('<img>', {'src': photo.url}),
                    $('<button>').text('Verwijder').on('click', () => {
                        delete_image(photo.id);
                    })
                )
            );
        })

        busy = false;
    }).fail(function (xhr, status, error) {
        $('#picture_container').html('');
        busy = false;
        fail_message($('#picture_container'), xhr);
    });
}

function delete_image(photo_id) {
    if (busy) return;
    if (!confirm('Weet u zeker dat u de afbeelding wilt verwijderen?')) return;
    busy = true;

    $.delete('/api/albums/'+ album_id +'/images/' + photo_id.toString() + '/', (data) => {
        create_message($('#error_container'), 'success', 'Afbeelding verwijderd', 'Het is gelukt om de afbeelding uit het album te verwijderen.')
        busy = false;
        show_images();
    }).fail(function (xhr, error, status) {
        busy = false;
        fail_message($('#error_container'), xhr);
    });
}

function upload_images() {
    if (busy) return;
    busy = true;

    const $file_input = $('#files')[0];
    const selected_files = $file_input.files;

    if (selected_files.length === 0) {
        create_message($('#upload_errors'), 'error', 'Geen bestanden geselecteerd', 'Selecteer ten minste 1 bestand om te uploaden.')
    }

    $('#add_button').attr('disabled', true);
    $('#add_button').addClass('disabled');

    var current_file = 0;
    var progress = 0;
    const progress_per_file = 100 / selected_files.length;

    $progress_bar = $('<span>').css('width', '0%');
    $('#progress_bar').append(
        $('<div>', {'class': 'meter'}).append($progress_bar)
    );

    failed_files = []

    const upload_file = () => {
        if (current_file < selected_files.length) {
            const send_data = new FormData();
            send_data.append('photo', selected_files[current_file], selected_files[current_file].name);

            $.ajax({
                type: 'POST',
                url: '/api/albums/'+ album_id +'/images/',
                success: function (data) {
                    progress += progress_per_file;
                    $progress_bar.css('width', progress.toString() + '%');
                    console.log(progress);
                    console.log($progress_bar)
                },
                error: function (xhr, status, error) {
                    failed_files.push({'code': xhr.status, 'name': selected_files[current_file].name});
                },
                complete: function (xhr, status) {
                    current_file++;
                    upload_file();
                },
                async: true,
                data: send_data,
                cache: false,
                contentType: false,
                processData: false,
                timeout: 60000,
            })


        } else {
            failed_files.forEach((failed_file) => {
                create_message($('#upload_errors'), 'error', 'Kon afbeelding niet uploaden', 'Het is niet gelukt om afbeelding ' + failed_file.name + ' te uploaden door foutcode ' + failed_file.code.toString());
            });

            $('#files').val('');
            $('#progress_bar').html('');
            $('#add_button').attr('disabled', false);
            $('#add_button').removeClass('disabled');
            busy = false;
            show_images();
        }
    }

    upload_file();

}