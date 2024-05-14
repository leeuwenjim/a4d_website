class NewsPagination {
    constructor(endpoint, $news_container, $navigation_container) {
        this.endpoint = endpoint;
        this.container = $news_container;
        this.navigation_container = $navigation_container;
        this.current_page = 1;
    }
    set_navigation(navigation_data) {
        this.navigation_container.html('');

        var $pagination_menu = $('<div>', {'class': 'pagination'});
        navigation_data.forEach((page_data) => {
            $pagination_menu.append(page_data['page']
                ?
                $('<div>', {'class': (this.current_page === page_data['page'] ? 'active item' : 'item')})
                    .text(page_data['page'].toString())
                    .on('click', () => {
                        this.load_page(page_data['page']);
                    })
                :
                $('<div>', {'class': 'disabled item'}).text('...'));
        });
        this.navigation_container.append($pagination_menu)
    }

    data_to_news_item(data) {

        return $('<div>', {'class': 'content-container'}).append(
            $('<h2>', {'class': 'news_header'}).text(data.title),
            $('<p>', {'class': 'small'}).text(data.published_on),
            $('<p>').html(data.content.replace(/(?:\r\n|\r|\n)/g, '<br />')),
            (data.link ?
                $('<a>', {'href': data.link}).text('Zie meer...')
                :
                $()
            )
        )
    }

    load_page(page_number) {
        this.container.html('');

        var send_data = {
            'page': page_number
        };

        $.get(this.endpoint, send_data, (data) =>{
            this.current_page = data['current'];
            data['results'].forEach((news_data) => {
                this.container.append(this.data_to_news_item(news_data));
            });
            this.set_navigation(data['navigation'])
        }).fail(function() {
            const error_text = 'Er was een probleem met het ophalen van de nieuws berichten';
            alert(error_text);
        });


    }

}
