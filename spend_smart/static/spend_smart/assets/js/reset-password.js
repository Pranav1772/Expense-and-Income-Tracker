const passwordField = document.getElementById("passwordField");
const passwordFeedbackArea = document.getElementById("password-feedback");
const confirmpasswordField = document.getElementById("confirm-password");
const btn = document.getElementById("button");

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

const validateField = (field, feedbackArea, url, fieldName) => {
    field.addEventListener("keyup", (e) => {
        const fieldVal = e.target.value;
        btn.disabled = !passwordField.value;
        if (fieldVal.length > 0) {
            fetch(url, {
                body: JSON.stringify({ [fieldName]: fieldVal }),
                method: "POST",
                headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
            })
                .then((res) => res.json())
                .then((data) => {
                    field.classList.remove("is-invalid");
                    feedbackArea.innerHTML = "";
                    if (data[`${fieldName}_error`]) {
                        btn.disabled = true;
                        field.classList.add("is-invalid");
                        feedbackArea.innerHTML = data[`${fieldName}_error`];
                        if (fieldName === "password") {
                            feedbackArea.style.display = "block";
                        }
                    } else {
                        btn.disabled = !passwordField.value;
                    }
                });
        }
    });
};

validateField(passwordField, passwordFeedbackArea, "/spendsmart/authentication/validate-password/", "password");
