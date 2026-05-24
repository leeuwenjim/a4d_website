
var busy = false;
var modal_showing = false;
const img_div = $('#extra_img_div');

document.addEventListener("DOMContentLoaded", function(event) {
    load_images();
});

$(document).on('click', '.img-card img', function () {
    const src = $(this).attr('src');
    const alt = $(this).attr('alt');
    $('#img-preview-large').attr('src', src).attr('alt', alt);
    $('#img-preview-modal').fadeIn(200);
});

$(document).on('click', '#img-preview-backdrop, #img-preview-large', function () {
    $('#img-preview-modal').fadeOut(200);
});

function load_images()
{
    if (busy) {
        return;
    }
    busy = true;

    $.get('/api/route/extra/', {}, (data) => 
        {
            img_div.html('');
            data.forEach(item => {
                const card = $(`
                    <div class="img-card" data-id="${item.id}">
                        <p class="img-title">${item.title}</p>
                        <img src="${item.img_url}" alt="${item.title}" />
                        <div class="img-actions">
                            <button class="edit_button" data-id="${item.id}" data-action="title">
                                Titel aanpassen
                            </button>
                            <button class="edit_button" data-id="${item.id}" data-action="image">
                                Afbeelding wijzigen
                            </button>
                            <button class="delete_button" data-id="${item.id}">
                                Verwijder
                            </button>
                        </div>
                    </div>
                `);
                img_div.append(card);
            });
            busy = false;
        }
    );
}

$(document).on('click', '.delete_button', function () {
    if (busy) return;
    const item_id = String($(this).data('id'));

    if (!confirm('Are you sure you want to delete this image?')) return;

    const endpoint = '/api/route/extra/' +item_id+ '/';
    $.delete(endpoint, {}, (data) => {
            busy = false;
            $(`[data-id="${item_id}"]`).fadeOut(200, function () {
                $(this).remove();
            });
        }).fail(function (xhr, status, error) {
            busy = false;
            alert('Failed to delete. Please try again.')
        });

});

$(document).on('click', '.edit_button[data-action="title"]', function () {
    if (modal_showing) return;
    modal_showing = true;
    const item_id = $(this).data('id');
    const card = $(`[data-id="${item_id}"]`);
    const endpoint = '/api/route/extra/' + item_id.toString() + '/';

    new Modal({
        'modal': $('#image_title_edit'),
        'onShow': (modal_object) => {
            $.get(endpoint, {}, (data) => {
                $('#input_edit_title').val(data.title);
            }).fail(function (xhr, status, error) {
                modal_object.disable_buttons();
                fail_message($('#title_modal_error_container'), xhr);
            });
        },
        'onAccept': (modal_object) => {
            modal_object.disable_buttons();
            
            const send_data = {
                'title': $('#input_edit_title').val(),
            };
            $.put(endpoint, send_data, (data) => {
                card.find('.img-title').text(data.title);
                modal_object.close();
            }).fail(function (xhr, status, error) {
                modal_object.disable_buttons();
                fail_message($('#title_modal_error_container'), xhr);
            });

            return false;
        },
        'onHide': (modal_object) => {
            $('#input_edit_title').val('');
            modal_object.enable_buttons();
            modal_showing = false;
        },
    }).show();
});

function add_image()
{
    new Modal({
        'modal': $('#image_add_modal'),
        'onShow': (modal_object) => {
            $('#input_add_title').val('');
            $('#input_add_image').val('');
            
        },
        'onAccept': (modal_object) => {
            modal_object.disable_buttons();

            try{
            const send_data = new FormData();
            send_data.append('image', $('#input_add_image')[0].files[0], $('#input_add_image')[0].files[0].name);
            send_data.append('title', $('#input_add_title').val());

            $.ajax({
                type: 'POST',
                url: '/api/route/extra/',
                success: function (data) {
                    
                const card = $(`
                    <div class="img-card" data-id="${data.id}">
                        <p class="img-title">${data.title}</p>
                        <img src="${data.img_url}" alt="${data.title}" />
                        <div class="img-actions">
                            <button class="edit_button" data-id="${data.id}" data-action="title">
                                Titel aanpassen
                            </button>
                            <button class="edit_button" data-id="${data.id}" data-action="image">
                                Afbeelding wijzigen
                            </button>
                            <button class="delete_button" data-id="${data.id}">
                                Verwijder
                            </button>
                        </div>
                    </div>
                `);
                img_div.append(card);
                    modal_object.close();
                },
                error: function (xhr, status, error) {
                    fail_message($('#add_modal_error_container'), xhr);
                    modal_object.enable_buttons();
                },
                async: true,
                data: send_data,
                cache: false,
                contentType: false,
                processData: false,
                timeout: 60000,
            });
            
            } catch(error) 
            {
                create_message($('#add_modal_error_container'), 'error', "Geen afbeelding geselecteerd", "Er is iets misgegaan, heeft u wel een afbeelding geselecteerd?");
                modal_object.enable_buttons();
            }
            return false;
        },
        'onHide': (modal_object) => {
            $('#input_add_title').val('');
            $('#input_add_image').val('');
            modal_object.enable_buttons();
            modal_showing = false;
        },
    }).show();
}

$(document).on('click', '.edit_button[data-action="image"]', function () {
    if (modal_showing) return;
    modal_showing = true;
    const item_id = $(this).data('id');
    const card = $(`[data-id="${item_id}"]`);
    const endpoint = '/api/route/extra/' + item_id.toString() + '/';

    new Modal({
        'modal': $('#image_swap_modal'),
        'onShow': (modal_object) => {
            $('#input_swap_image').val('');
            
        },
        'onAccept': (modal_object) => {
            modal_object.disable_buttons();

            const send_data = new FormData();
            try{
                send_data.append('image', $('#input_swap_image')[0].files[0], $('#input_swap_image')[0].files[0].name);
                $.ajax({
                type: 'POST',
                url: endpoint,
                success: function (data) {
                    card.find('img').attr('src', data.img_url);
                    modal_object.close();
                },
                error: function (xhr, status, error) {
                    fail_message($('#swap_modal_error_container'), xhr);
                    modal_object.enable_buttons();
                },
                async: true,
                data: send_data,
                cache: false,
                contentType: false,
                processData: false,
                timeout: 60000,
            });
            } catch(error) 
            {
                create_message($('#swap_modal_error_container'), 'error', "Geen afbeelding geselecteerd", "Er is iets misgegaan, heeft u wel een afbeelding geselecteerd?");
                modal_object.enable_buttons();
            }
            return false;
        },
        'onHide': (modal_object) => {
            $('#input_add_image').val('');
            modal_object.enable_buttons();
            modal_showing = false;
        },
    }).show();
});


