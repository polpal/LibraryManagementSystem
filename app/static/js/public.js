$(document).ready(function () {
    console.log("Public books JavaScript loaded.");

    const searchInput = $("#publicBookSearch");
    const resultsContainer = $("#publicBookResults");

    let searchTimer;

    searchInput.on("input", function () {
        clearTimeout(searchTimer);

        const search = searchInput.val().trim();

        searchTimer = setTimeout(function () {
            $.ajax({
                url: searchInput.closest("form").attr("action"),
                type: "GET",
                data: {
                    search: search,
                    page: 1,
                },
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
                success: function (response) {
                    console.log("AJAX request successful.");

                    resultsContainer.html(response);

                    searchInput.focus();
                },
                error: function () {
                    console.log("AJAX request failed.");
                },
            });
        }, 300);
    });
});

$(document).on("click", "#publicBookResults .page-link", function (event) {
    event.preventDefault();

    const url = $(this).attr("href");

    $.ajax({
        url: url,
        type: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
        success: function (response) {
            console.log("Pagination AJAX successful.");

            $("#publicBookResults").html(response);

            $("#publicBookSearch").focus();
        },
        error: function () {
            console.log("Pagination AJAX failed.");
        },
    });
});
