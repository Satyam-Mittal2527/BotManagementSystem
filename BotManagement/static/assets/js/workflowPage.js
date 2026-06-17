function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {

        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {

            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;
            }
        }
    }

    return cookieValue;
}
async function runWorkflow(workflowId) {

    await fetch(

        `/workflow/run/${workflowId}/`

    )

    alert(
        "Workflow Started"
    )

}
document.querySelectorAll(".run-btn").forEach(button => {

    button.addEventListener("click", async function () {



        const workflowId = this.dataset.workflowId;

        const run_btn = this;

        // Change appearance while running
        run_btn.innerHTML = "RUNNING";
        run_btn.style.backgroundColor = "green";
        run_btn.disabled = true;

        const response = await fetch(
            `/workflow/run/${workflowId}`
        );

        const result = await response.json();

        // console.log(result);

        // Restore button
        run_btn.innerHTML = "RUN";
        run_btn.style.backgroundColor = "";
        run_btn.disabled = false;

        alert("Workflow Execution Complete");

    });

});

document.querySelectorAll(".delete-btn").forEach(button => {

    button.addEventListener("click", async function () {

        // console.log("WorkflowID", this.dataset)
        const workflowId = this.dataset.workflowId;


        const response = await fetch(
            `/workflow/delete/${workflowId}/`
        )

        const result = await response.json();

        // console.log(result);

        // Update UI immediately
        alert("Workflow Deleted")
    });

});

function viewHistory(workflowId) {
    // console.log(workflowId)

    window.location.href =

        `/workflowHistory/${workflowId}/`

}


async function deleteWorkflow(workflowId) {

    await fetch(

        `/workflow/delete/${workflowId}/`

    )

    loadWorkflows()

}

document.querySelectorAll(".view-btn").forEach(button => {
    button.addEventListener("click", async function () {
      
        const workflowName = this.dataset.workflowName;
       

        const response = await fetch(

            `/workflow/view/${workflowName}/`,
            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json",

                    "X-CSRFToken": getCookie(
                        "csrftoken"
                    )

                },

                body: JSON.stringify({

                    bot_name: workflowName

                })

            }

        );

        const html = await response.text();

        document.open();

        document.write(
            html
        );

        document.close();

    });

});