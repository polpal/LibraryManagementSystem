document.addEventListener("DOMContentLoaded", function () {
    const password = document.getElementById("password");
    const toggle = document.getElementById("togglePassword");

    if (password && toggle) {
        toggle.addEventListener("click", function () {
            const type = password.getAttribute("type") === "password" ? "text" : "password";

            password.setAttribute("type", type);
        });
    }
});
