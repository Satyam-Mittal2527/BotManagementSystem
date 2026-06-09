const EditBotForm = document.getElementById("EditBotForm");
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

EditBotForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const formData = new FormData();

    formData.append(
        "bot_name",
        document.getElementById("BotName").value
    );

    formData.append(
        "bot_code",
        document.getElementById("BotCode").value
    );

    try {

        const response = await fetch(
            "/api/EditBot",
            {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: formData
            }
        );

        const result = await response.json();

        console.log(result);

    }
    catch(error){

        console.log(error);

    }

});

// ======================
// Open file
// ======================

document.querySelectorAll(".file-btn").forEach(button => {

    button.addEventListener("click", async function () {

        const fileName = this.dataset.file;

        const botName = document.getElementById(
            "BotName"
        ).value;

        try {

            const response = await fetch(
                "/api/viewFile",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")
                    },

                    body: JSON.stringify(
                        {
                            bot_name: botName,
                            file_name: fileName
                        }
                    )
                }
            );

            const result = await response.json();

            console.log(result);

            if (result.status === "success") {

                // Update code editor
                document.getElementById(
                    "BotCode"
                ).value = result.code;

                // Remember current file
                document.getElementById(
                    "CurrentFile"
                ).value = fileName;

            }

        }
        catch (error) {

            console.log(error);

        }

    });

});


// ======================
// Save file
// ======================



EditBotForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const formData = new FormData();

        formData.append(
            "bot_name",
            document.getElementById(
                "BotName"
            ).value
        );

        formData.append(
            "bot_code",
            document.getElementById(
                "BotCode"
            ).value
        );

        formData.append(
            "file_name",
            document.getElementById(
                "CurrentFile"
            ).value
        );

        try {

            const response = await fetch(
                "/api/EditBot",
                {
                    method: "POST",

                    headers: {
                        "X-CSRFToken":
                        getCookie("csrftoken")
                    },

                    body: formData
                }
            );

            const result =
                await response.json();

            console.log(result);

        }
        catch (error) {

            console.log(error);

        }

    }
);