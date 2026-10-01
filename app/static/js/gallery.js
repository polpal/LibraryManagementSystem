$(document).ready(function () {
    const galleryImages = $(".gallery-image");
    const modalImage = $("#galleryModalImage");

    let currentIndex = 0;

    function showImage(index) {
        currentIndex = index;

        const imageUrl = galleryImages.eq(currentIndex).attr("src");

        modalImage.attr("src", imageUrl);
    }

    galleryImages.on("click", function () {
        currentIndex = galleryImages.index(this);

        showImage(currentIndex);

        const galleryModal = new bootstrap.Modal(document.getElementById("galleryModal"));

        galleryModal.show();
    });

    $("#galleryPrevious").on("click", function () {
        currentIndex--;

        if (currentIndex < 0) {
            currentIndex = galleryImages.length - 1;
        }

        showImage(currentIndex);
    });

    $("#galleryNext").on("click", function () {
        currentIndex++;

        if (currentIndex >= galleryImages.length) {
            currentIndex = 0;
        }

        showImage(currentIndex);
    });
});
