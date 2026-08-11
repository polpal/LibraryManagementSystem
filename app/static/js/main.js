console.log("Library Management System JavaScript loaded.");

$(document).ready(function () {

    // Books DataTable
    if ($('#booksTable').length) {

        $('#booksTable').DataTable({
            pageLength: 10,
            language: {
                emptyTable: "No books are currently available."
            }
        });

    }


    // Issued Books DataTable
    if ($('#issuedBooksTable').length) {

        $('#issuedBooksTable').DataTable({
            pageLength: 10,
            language: {
                emptyTable: "No books are currently issued."
            }
        });

    }

});