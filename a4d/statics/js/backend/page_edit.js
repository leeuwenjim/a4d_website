var editor = null;
var slug = ''

document.addEventListener("DOMContentLoaded", function (event) {

    slug = window.location.pathname.match(/([^\/]*)\/*$/)[1];

    editor = new EditorJS({
        holder: 'editorjs',
        inlineToolbar: ['link', 'bold', 'italic'],
        tools: {
            header: {
                class: Header,
                inlineToolbar: ['link'],
                config: {
                    placeholder: 'Header'
                },
                shortcut: 'CMD+SHIFT+H'
            },

            list: {
                class: List,
                inlineToolbar: true,
                shortcut: 'CMD+SHIFT+L'
            },

            table: {
                class: Table,
                inlineToolbar: true,
                shortcut: 'CMD+ALT+T'
            },
            delimiter: Delimiter,

        }
    });
    editor.isReady
        .then(() => {
            $('#editor_container').css('display', 'block');
            $.get('/api/' + slug + '/', {}, (data) => {
                const blocks = JSON.parse(data['blocks'])
                if (blocks.length > 0) {
                    const page_data = {
                        'time': new Date().getTime(),
                        'version': '2.28.2',
                        'blocks': blocks,
                    }
                    editor.render(page_data);
                }
            }).fail(function (xhr, status, error) {
                fail_message($('#error_container', xhr));
            })
        })
        .catch((reason) => {
            alert(`Editor initialization failed because of ${reason}`);
            $('#add_button').css('color', '#2A4C2A').css('background-color', '#417541').attr('disabled', true);
        });

});

function save_editor() {
    editor.save().then((save_data) => {
        $.post('/api/' + slug + '/', {'data': JSON.stringify(save_data.blocks)}, (data) => {
            create_message($('#error_container'), 'success', 'Gegevens zijn opgeslagen', 'De veranderingen zijn opgeslagen en zijn voor iedereen zichtbaar.')
        }).fail(function (xhr, status, error) {
            fail_message($('#error_container'), xhr);
        })
    });
}
