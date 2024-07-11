// const searchField = document.getElementById("searchfield");
// const getCookie = (name) => {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== "") {
//         const cookies = document.cookie.split(";");
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === name + "=") {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// };

// searchField.addEventListener("keyup", (e) => {
//     const searchValue = e.target.value;
//     if (searchValue.trim().length > 0) {
//         fetch("/expenses/search-expenses", {
//             body: JSON.stringify({ searchText: searchValue }),
//             method: "POST",
//             headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
//         })
//             .then((res) => res.json())
//             .then((data) => {
//                 console.log(data);
//                 if(data.length==0){

//                 }
//             });
//     }
// });
