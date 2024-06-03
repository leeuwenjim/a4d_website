document.addEventListener("DOMContentLoaded", function (event) {
    gridGallery({
        selector: ".gg-box",
        darkMode: false,
        layout: "square",
        gapLength: 100,
        rowHeight: 200,
        columnWidth: 200,
    });

    var isSafari = navigator.vendor && navigator.vendor.indexOf('Apple') > -1 &&
        navigator.userAgent &&
        navigator.userAgent.indexOf('CriOS') == -1 &&
        navigator.userAgent.indexOf('FxiOS') == -1;

    if (isSafari) {
        var images = document.getElementsByClassName('gallery_image')
        for (var i = 0; i < images.length; i++) {
            images[i].style.margin = '2px';
        }
    }

});

