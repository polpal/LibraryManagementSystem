document.addEventListener("DOMContentLoaded", function () {
    const profilePicture = document.getElementById("profilePicture");

    const imagePreview = document.getElementById("imagePreview");
    if (profilePicture) {
        profilePicture.addEventListener("change", function (event) {
            const file = event.target.files[0];

            if (file) {
                const reader = new FileReader();

                reader.onload = function (e) {
                    imagePreview.src = e.target.result;

                    imagePreview.style.display = "block";
                };

                reader.readAsDataURL(file);
            }
        });
    }
});
