function menu_function() {
    var x = document.getElementById("menu");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}

function dropdown_click_info() {
    document.getElementById("info_dropdown").classList.toggle("show");
}

function dropdown_click_about() {
    document.getElementById("about_dropdown").classList.toggle("show");
}

document.addEventListener("DOMContentLoaded", function (event) {
    window.onclick = function (event) {
        var dropdown_menu_id = '';
        try {
            dropdown_menu_id = event.target.nextElementSibling.id;
        } catch (error) {

        }

        if (dropdown_menu_id != 'info_dropdown') {
            const info_dropdown = document.getElementById("info_dropdown");
            if (info_dropdown.classList.contains('show')) {
                info_dropdown.classList.remove('show')
            }
        }

        if (dropdown_menu_id != 'about_dropdown') {
            const about_dropdown = document.getElementById("about_dropdown");
            if (about_dropdown.classList.contains('show')) {
                about_dropdown.classList.remove('show')
            }
        }
    }
});