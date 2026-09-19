document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll("form[data-loader]").forEach(function (form) {

        form.addEventListener("submit", function () {

            const button = form.querySelector(
                'button[type="submit"], input[type="submit"]'
            );

            if (!button) {
                return;
            }

            const loadingText = form.dataset.loader || "Processing...";

            button.disabled = true;

            if (button.tagName === "BUTTON") {

                button.innerHTML = `
                    <span class="spinner-border spinner-border-sm me-2"
                          role="status"
                          aria-hidden="true"></span>
                    ${loadingText}
                `;

            } else {

                button.value = loadingText;

            }

        });

    });

});