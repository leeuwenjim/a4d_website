function create_message($container, type, title, text) {
    $container.prepend(
        $('<div>', {'class': 'message ' + type}).append(
            $('<span>', {'class': 'message_close_btn'}).html('&times;').on('click', function (e) {
                $(this).parent().remove();
            }),
            $('<h2>').text(title),
            $('<p>').html(text)
        )
    );
}

function fail_message($container, xhr) {
    var title = ''
    var message = ''
    if (xhr.status === 400) {
        title = 'Fout met gegevens';
        message = 'Er is een fout met de verzonden gegevens. <br />';

        Object.entries(xhr.responseJSON).forEach((entry) => {
            const [key, value] = entry;
            message += `${key}: ${value}<br />`;
        })
    } else if (xhr.status === 404) {
        title = 'Object niet gevonden';
        message = 'Helaas is het object niet op de server gevonden. Probeer de pagina te herladen.';
    } else if (xhr.status > 400 && xhr.status < 500) {
        title = 'Geen permissie';
        message = 'Helaas heeft u momenteel geen permissie om deze actie uit te voeren. Probeer eventueel opnieuw aanmelden.';
    } else {
        title = 'Serverfout';
        message = 'Er is op de server iets misgegaan met opslaan';
    }

    create_message($container, 'error', title, message)
}