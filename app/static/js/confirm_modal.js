document.addEventListener("DOMContentLoaded", function () {
    const confirmModalElement = document.getElementById("confirmModal");

    if (!confirmModalElement) {
        return;
    }

    const confirmModal = new bootstrap.Modal(confirmModalElement);

    const modalTitle = document.getElementById("confirmModalLabel");
    const modalMessage = document.getElementById("confirmModalMessage");
    const modalForm = document.getElementById("confirmModalForm");
    const modalButton = document.getElementById("confirmModalButton");

    document.querySelectorAll(".confirm-modal-trigger").forEach(function (button) {
        button.addEventListener("click", function () {
            const title = this.dataset.modalTitle;
            const message = this.dataset.modalMessage;
            const action = this.dataset.modalAction;
            const confirmText = this.dataset.modalConfirm || "Confirm";

            modalTitle.textContent = title;
            modalMessage.textContent = message;
            modalForm.action = action;
            modalButton.textContent = confirmText;

            confirmModal.show();
        });
    });
});
