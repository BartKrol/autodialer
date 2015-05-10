'use strict';
(function () {
    $("#search-peer").keypress(function (e) {
        if (e.which == 13) {
            var searchText = $("#search-peer").val();
            window.location.replace(window.location.pathname + "/search/" + searchText);
        }
    });
})();

