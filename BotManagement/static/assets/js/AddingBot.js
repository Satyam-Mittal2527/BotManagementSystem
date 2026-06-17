// console.log("main.js loaded");

const BotForm = document.getElementById("NewBotForm");
const BotMessage = document.querySelector(".NewBotAdditionResult")
// console.log(BotForm)
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
BotForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const formData = new FormData();

    formData.append("first_name", document.getElementById("firstName").value);
    formData.append("last_name", document.getElementById("lastName").value);
    formData.append("bot_name", document.getElementById("botName").value);
    formData.append("branch", document.getElementById("branch").value);
    formData.append("status", "INACTIVE");
    const scriptFile = document.getElementById("ScriptFile").files;
    const botFolder = document.getElementById("BotFolder").files;
    const helperFiles = document.getElementById("HelperFolder").files;
    // for (let i = 0; i < helperFiles.length; i++) {
    //     console.log(helperFiles[i].name);
    //     console.log(helperFiles[i].webkitRelativePath);
    // }
    for (let i = 0; i < helperFiles.length; i++) {
        formData.append("helper_files", helperFiles[i]);
        formData.append(
            "helper_paths",
            helperFiles[i].webkitRelativePath
        );
    }

    // console.log(helperFiles);
    // console.log(helperFiles.length);
    if (scriptFile.length > 0) {

        formData.append("upload_type", "file");

        formData.append("script_files", scriptFile[0]);

    }
    else if (botFolder.length > 0) {

        formData.append("upload_type", "folder");

        formData.append("folder_name", prompt("Enter bot folder name"));

        for (const file of botFolder) {
            formData.append("script_files", file);
        }

    }
    try {

        const response = await fetch("/api/NewBot", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: formData
        });

        const result = await response.json();

        // console.log(result);

    } catch (error) {
        console.log(error);
    }

});
