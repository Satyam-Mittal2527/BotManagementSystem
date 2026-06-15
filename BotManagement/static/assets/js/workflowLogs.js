let runId = window.location.pathname.split("/")[2]


async function loadLogs() {

    let response = await fetch(

        `/workflow/logs/${runId}/`

    )

    let data = await response.json()

    console.log(data)

    let logsDiv = document.getElementById(

        "logs"

    )

    logsDiv.innerHTML = ""

    data.logs.forEach(

        log => {

            logsDiv.innerHTML += `

            <tr>

                <td>

                    ${log.node_id}

                </td>

                <td>

                    ${log.log_level}

                </td>

                <td>

                    ${log.message}

                </td>

                <td>

                    ${log.created_at}

                </td>
            </tr>

            `

        }

    )

}

loadLogs()