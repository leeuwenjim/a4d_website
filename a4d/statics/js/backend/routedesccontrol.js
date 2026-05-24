
document.addEventListener("DOMContentLoaded", function(event) {
    load_data("1");
});

function save_desc()
{
    const activeId = String(document.querySelector('.group-button.active').dataset.id);
    const endpoint = "/api/route/routes/"+activeId+"/";

    $.post(
        endpoint,
        {
            "description": $("#alter_desc_field").val()
        },
        (data) =>
        {
            create_message($('#error_container'), 'success', 'Aanpassing is opgeslagen', 'De aanpassingen in de route beschrijving zijn succesvol opgeslagen.');
        }
    ).fail(function (xhr, status, error){
        fail_message($('#error_container'), xhr);
    });
}

function upload_image()
{
    const $file_input = $('#route_img_file')[0];
    const selected_files = $file_input.files;

    if (selected_files.length > 0)
    {
        const activeId = String(document.querySelector('.group-button.active').dataset.id);
        const endpoint = "/api/route/routes/"+activeId+"/img/";
        const send_data = new FormData();
        send_data.append('image', selected_files[0], selected_files[0].name);

        $.ajax({
            type: 'POST',
            url: endpoint,
            success: function (data) {
                $("#img_preview").html("");
                $("#img_preview").append(
                    $("<img>", {'src': data.img_url})
                );
            },
            error: function (xhr, status, error) {
                fail_message($('#error_container'), xhr);
            },
            async: true,
            data: send_data,
            cache: false,
            contentType: false,
            processData: false,
            timeout: 60000,
        });
    }
    else {
        create_message($('#error_container'), 'error', 'Selecteer een afbeelding', 'Er was geen afbeelding geselecteerd om te uploaden');
    }
}

function delete_image()
{
    if (!confirm('Weet u zeker dat u de afbeelding wilt verwijderen?')) return;
    const activeId = String(document.querySelector('.group-button.active').dataset.id);
    const endpoint = "/api/route/routes/"+activeId+"/img/";
    $.delete(endpoint, {}, (data) => {$("#img_preview").html("");}).fail(function (xhr, status, error){
        fail_message($('#error_container'), xhr);
    });
}

function load_data(item_id)
{
    const endpoint = "/api/route/routes/"+item_id+"/"

        // OPTIONAL: add loader to alter_header
    $.get(endpoint, {}, (data) => {
        // Set data
            $("#alter_header").text(data.title);
        $("#alter_desc_field").val(data.description);
        if (data.img_url !== '')
        {
            $("#img_preview").append(
                $("<img>", {'src': data.img_url})
            );
        }
        

    }).fail(function (xhr, status, error){
        // OPTIONAL remove loader

        $("#alter_header").text('Kon data niet ophalen');
    });
}

const group = document.getElementById('my-group');
group.querySelectorAll('.group-button').forEach(btn => {
    btn.addEventListener('click', () => {
        group.querySelectorAll('.group-button').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // First clear everything 
        $("#alter_header").text("");
        $("#alter_desc_field").val("");
        $("#route_img_file").val("");
        $("#img_preview").html("");

        const item_id = String($(btn).data("id"));
        load_data(item_id);
    });
});