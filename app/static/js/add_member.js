const nameInput = document.getElementById("name");
const nameError = document.getElementById("nameError");
const saveButton = document.getElementById("saveButton");
const emailInput = document.getElementById("email");
const emailError = document.getElementById("emailError");
const phoneInput = document.getElementById("phone");
const phoneError = document.getElementById("phoneError");

function validateName() {
    const name = nameInput.value.trim();

    if (name === "") {
        setFieldState(nameInput, nameError, false, "Name is required.");

        return false;
    }

    if (name.length < 2) {
        setFieldState(nameInput, nameError, false, "Name must contain at least 2 characters.");

        return false;
    }

    if (!/^[\p{L}\p{M} .'-]+$/u.test(name)) {
        setFieldState(nameInput, nameError, false, "Name contains invalid characters.");

        return false;
    }

    setFieldState(nameInput, nameError, true);

    return true;
}

function setFieldState(input, errorElement, isValid, message = "") {
    if (isValid) {
        input.classList.remove("is-invalid");
        input.classList.add("is-valid");
        return;
    }

    input.classList.remove("is-valid");
    input.classList.add("is-invalid");
    errorElement.textContent = message;
}

function updateFormState() {
    const nameValid = validateName();
    const emailValid = validateEmail();
    const phoneValid = validatePhone();

    saveButton.disabled = !(nameValid && emailValid && phoneValid);
}
function validateEmail() {
    const email = emailInput.value.trim();

    if (email === "") {
        setFieldState(emailInput, emailError, false, "Email is required.");

        return false;
    }

    if (!emailInput.checkValidity()) {
        setFieldState(emailInput, emailError, false, "Please enter a valid email address.");

        return false;
    }
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(email)) {
        setFieldState(emailInput, emailError, false, "Please enter a valid email address.");

        return false;
    }

    setFieldState(emailInput, emailError, true);

    return true;
}
function validatePhone() {
    const phone = phoneInput.value.trim();

    if (phone === "") {
        phoneInput.classList.add("is-invalid");
        phoneInput.classList.remove("is-valid");
        phoneError.textContent = "Phone number is required.";

        return false;
    }

    if (!/^\d{10}$/.test(phone)) {
        phoneInput.classList.add("is-invalid");
        phoneInput.classList.remove("is-valid");
        phoneError.textContent = "Phone number must contain exactly 10 digits.";

        return false;
    }

    phoneInput.classList.remove("is-invalid");
    phoneInput.classList.add("is-valid");

    return true;
}
nameInput.addEventListener("input", updateFormState);
emailInput.addEventListener("input", updateFormState);
phoneInput.addEventListener("input", function () {
    this.value = this.value.replace(/\D/g, "");

    updateFormState();
});
