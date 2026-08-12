console.log("Library Management System JavaScript loaded.");

$(document).ready(function () {
    if ($("#booksTable").length) {
        $("#booksTable").DataTable({
            pageLength: 10,
            lengthMenu: [10, 25, 50, 100],

            order: [[2, "asc"]],

            language: {
                emptyTable: "No books are currently available.",
                zeroRecords: "No matching books found.",
            },
        });
    }

    if ($("#issuedBooksTable").length) {
        $("#issuedBooksTable").DataTable({
            pageLength: 10,
            lengthMenu: [10, 25, 50, 100],

            language: {
                emptyTable: "No books are currently issued.",
                zeroRecords: "No matching issued books found.",
            },
        });
    }
});
