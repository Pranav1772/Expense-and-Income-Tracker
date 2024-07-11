const emailField = document.getElementById("emailField");
const emailFeedbackArea = document.getElementById("email-feedback");
const signupBtn = document.getElementById("send-link");

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
        signupBtn.disabled = !emailField.value;
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
                        signupBtn.disabled = true;
                        field.classList.add("is-invalid");
                        feedbackArea.innerHTML = data[`${fieldName}_error`];
                        if (fieldName === "password") {
                            feedbackArea.style.display = "block";
                        }
                    } else {
                        signupBtn.disabled = !emailField.value;
                    }
                });
        }
    });
};

validateField(emailField, emailFeedbackArea, "/spendsmart/authentication/validate-reset-email/", "email");
