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

let path = window.location.pathname

let workflowId = path.split("/")[2]


async function loadHistory() {

    let response = await fetch(

        `/workflow/history/${workflowId}/`

    )

    let data = await response.json()

    let runs = data.workflow_runs

    let table = document.getElementById(

        "history_table"

    )

    table.innerHTML = ""

    runs.forEach(

        run => {

            table.innerHTML += `

            <tr>

                <td>

                    ${run.id}

                </td>

                <td class="${run.status}">

                    ${run.status}

                </td>

                <td>

                    ${run.started_at}

                </td>

                <td>

                    ${run.ended_at}

                </td>
                 <td>
                    <button class="view-btn" data-workflow-runId="${run.id}">
                        View Logs
                    </button>
                </td>

            </tr>

            `

        }

    )
    document.querySelectorAll(".view-btn").forEach(button => {

        button.addEventListener("click", async function () {
            // console.log(this.dataset)
            const workflowRunId =
                this.dataset.workflowRunid;
            // console.log(workflowRunId)
            window.location.href =

                `/workflowLogs/${workflowRunId}/`

        });

    });
}



loadHistory()