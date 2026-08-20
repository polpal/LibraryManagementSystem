document.addEventListener("DOMContentLoaded", function () {
    const flashMessages = document.querySelectorAll(".flash-message");

    flashMessages.forEach(function (message) {
        setTimeout(function () {
            const alert = bootstrap.Alert.getOrCreateInstance(message);

            alert.close();
        }, 3000);
    });
});
