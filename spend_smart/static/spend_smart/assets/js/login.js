const usernameField = document.getElementById("usernameField");
const usernameFeedbackArea = document.getElementById("username-feedback");
const passwordField = document.getElementById("passwordField");
const passwordFeedbackArea = document.getElementById("password-feedback");
const signinBtn = document.getElementById("signin-button");

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
        signinBtn.disabled = !(usernameField.value && passwordField.value);
        const fieldVal = e.target.value;
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
                        signinBtn.disabled = true;
                        field.classList.add("is-invalid");
                        feedbackArea.innerHTML = data[`${fieldName}_error`];
                        if (fieldName === "password") {
                            feedbackArea.style.display = "block";
                        }
                    } else {
                        signinBtn.disabled = !(usernameField.value && passwordField.value);
                    }
                });
        }
    });
};

validateField(usernameField, usernameFeedbackArea, "/spendsmart/authentication/is-username-valid/", "username");
validateField(passwordField, passwordFeedbackArea, "/spendsmart/authentication/validate-password/", "password");
