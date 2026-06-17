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

document.querySelectorAll(".run-btn").forEach(button => {

    button.addEventListener("click", async function () {

        const botId = this.dataset.botId;
  
        const payload = {
            botId
        };

        const response = await fetch("/api/runBot", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        // console.log(result);

        // Update UI immediately
        if (result.status === "Success") {

            document.getElementById(`status-${botId}`).innerHTML =
                `<span class="badge text-bg-success">
                    ACTIVE
                </span>`;

        }

    });

});

document.querySelectorAll(".stop-btn").forEach(button => {
    button.addEventListener("click", async function (){
        // console.log("Stop button Data",this.dataset)
        const botId = this.dataset.botId;
        
        const payload = {
            botId
        }
        const response = await fetch("/api/stopBot", {
            method: "POST",
            headers : {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify(payload)
        })

        // console.log("Request send stop success")
        const result = await response.json();
        // console.log(result);

    });
})

document.querySelectorAll(".view-btn").forEach(button => {

    button.addEventListener("click", async function () {

        const botName = this.dataset.botName;

        const response = await fetch("/api/viewBot", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                bot_name: botName
            })
        });

        const html = await response.text();

        document.open();
        document.write(html);
        document.close();

    });

});
function ExportLogs(runId){
    // console.log(runId);
    window.location.href = `/api/exportLogs/${runId}`;
}