const DeleteForm = document.getElementById("DeleteBotForm")
function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;
            }
        }
    }

    return cookieValue;
}
DeleteForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = new FormData();

    formData.append("bot_name", document.getElementById("BotName").value);

    try {

        const response = await fetch("/api/DeleteBot", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: formData
        });

        const result = await response.json();

        console.log(result);

    } catch (error) {
        console.log(error);
    }
})