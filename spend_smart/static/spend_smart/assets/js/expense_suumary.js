const renderchat = (data, labels) => {
    const ctx = document.getElementById("myChart");
    new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Last 6 months expenses ",
                    data: data,
                    borderWidth: 1,
                },
            ],
        },
        options: {
            title: {
                responsive: true,
                maintainAspectRatio: false,
                display: true,
                text: "Expenses per category",
            },
        },
    });
};

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

const getChatsData = () => {
    fetch("/spendsmart/expenses/expense-category-summary", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
        .then((rese) => rese.json())
        .then((results) => {
            console.log(results);
            const category_data = results.expense_category_data;
            const [labels, data] = [Object.keys(category_data), Object.values(category_data)];
            renderchat(data, labels);
        });
};

document.onload = getChatsData();
