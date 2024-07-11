const renderchat = (data, labels) => {
    const ctx = document.getElementById("myChart");
    new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Last 6 months sources ",
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
    fetch("/spendsmart/incomes/income-source-summary/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
        .then((rese) => rese.json())
        .then((results) => {
            console.log(results);
            const source_data = results.income_source_data;
            const [labels, data] = [Object.keys(source_data), Object.values(source_data)];
            renderchat(data, labels);
        });
};

document.onload = getChatsData();
