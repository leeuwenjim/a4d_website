
var busy = false;
var album_id = '0';

const input     = document.getElementById('files');
const dropZone  = document.getElementById('drop-zone');
const fileList  = document.getElementById('file-list');
const emptyHint = document.getElementById('empty-hint');
const uploadBtn = document.getElementById('add_button');
let stagedFiles = [];

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


    if (stagedFiles.length === 0) {
        create_message($('#upload_errors'), 'error', 'Geen bestanden geselecteerd', 'Selecteer ten minste 1 bestand om te uploaden.')
    }

    $('#add_button').attr('disabled', true);
    $('#add_button').addClass('disabled');

    var current_file = 0;
    var progress = 0;
    const progress_per_file = 100 / stagedFiles.length;

    $progress_bar = $('<span>').css('width', '0%');
    $('#progress_bar').append(
        $('<div>', {'class': 'meter'}).append($progress_bar)
    );

    failed_files = []

    const upload_file = () => {
        if (current_file < stagedFiles.length) {
            const send_data = new FormData();
            send_data.append('photo', stagedFiles[current_file], stagedFiles[current_file].name);

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

            //$('#files').val('');
            $('#progress_bar').html('');
            $('#add_button').attr('disabled', false);
            $('#add_button').removeClass('disabled');
            busy = false;
            stagedFiles = [];
            renderList();
            show_images();
        }
    }

    upload_file();

}

function formatSize(bytes) {
    if (bytes < 1024)             return bytes + ' B';
    if (bytes < 1024 * 1024)      return Math.round(bytes / 1024) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function isImage(file) {
    return file.type.startsWith('image/');
}

function renderList() {
    fileList.innerHTML = '';

    if (stagedFiles.length === 0) {
    fileList.appendChild(emptyHint);
    uploadBtn.disabled = true;
    return;
    }

    uploadBtn.disabled = false;

    stagedFiles.forEach((file, index) => {
    const item = document.createElement('div');
    item.className = 'file-item';

    // Thumbnail
    const thumb = document.createElement('div');
    thumb.className = 'file-thumb';

    if (isImage(file)) {
        const img = document.createElement('img');
        img.alt = file.name;
        const reader = new FileReader();
        reader.onload = (e) => { img.src = e.target.result; };
        reader.readAsDataURL(file);
        thumb.appendChild(img);
    } else {
        // Fallback icon for non-image files that sneak past the accept filter
        const icon = document.createElement('span');
        icon.className = 'file-thumb-icon';
        icon.textContent = '🖼';
        thumb.appendChild(icon);
    }

    // Info
    const info = document.createElement('div');
    info.className = 'file-info';
    info.innerHTML = `
        <div class="file-name">${file.name}</div>
        <div class="file-size">${formatSize(file.size)}</div>
    `;

    // Remove button
    const remove = document.createElement('button');
    remove.className = 'file-remove';
    remove.setAttribute('aria-label', `Remove ${file.name}`);
    remove.textContent = '✕';
    remove.addEventListener('click', () => {
        stagedFiles.splice(index, 1);
        renderList();
    });

    item.appendChild(thumb);
    item.appendChild(info);
    item.appendChild(remove);
    fileList.appendChild(item);
    });
}

function addFiles(newFiles) {
    const filtered = Array.from(newFiles).filter((incoming) => {
    const duplicate = stagedFiles.some(
        (existing) => existing.name === incoming.name && existing.size === incoming.size
    );
    return !duplicate && isImage(incoming);
    });
    stagedFiles = [...stagedFiles, ...filtered];
    renderList();
}

input.addEventListener('change', () => {
    addFiles(input.files);
    // Reset the input so the same file can be re-added after removal
    input.value = '';
});
dropZone.addEventListener('dragenter', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault(); // required to allow drop
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', (e) => {
    // Only remove the class when leaving the drop zone entirely
    if (!dropZone.contains(e.relatedTarget)) {
    dropZone.classList.remove('drag-over');
    }
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    addFiles(e.dataTransfer.files);
});