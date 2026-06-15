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
let editor;
document.addEventListener("DOMContentLoaded", function () {

    const drawflow = document.getElementById("drawflow");

    console.log("drawflow =", drawflow);

    editor = new Drawflow(drawflow);

    editor.start();

    console.log(editor.precanvas);

    editor.precanvas.addEventListener("drop", drop);

    editor.precanvas.addEventListener("dragover", allowDrop);

});
function drag(ev) {

    ev.dataTransfer.setData(

        "node",

        ev.target.getAttribute(

            "data-node"

        )

    )

}
function allowDrop(ev) {

    ev.preventDefault()

}
function drop(ev) {
    console.log("Dropped")

    ev.preventDefault()

    ev.stopPropagation()

    let name = ev.dataTransfer.getData(
        "node"
    )

    addNodeToDrawFlow(

        name,

        ev.clientX,

        ev.clientY

    )

}
function addNodeToDrawFlow(

    name,

    pos_x,

    pos_y

) {

    const rect = editor.precanvas.getBoundingClientRect()

    pos_x = pos_x - rect.x

    pos_y = pos_y - rect.y


    editor.addNode(

        name,

        1,

        1,

        pos_x,

        pos_y,

        "script-node",

        {

            node_name: "",

            script_name: "",

            script_path: ""

        },

        `

        <div class="script-node-content">

            <h5>Script Node</h5>

            <input

                class="node-input"

                type="text"

                placeholder="Node Name"

                style="width:100%"

            >

            <br><br>

            <label class="node-button">

                Upload Script

                <input

                    type="file"

                    class="script-file"

                    hidden

                >

            </label>

            <p class="script-name">

                No file selected

            </p>

        </div>

        `,

        false

    );

}
document.addEventListener(

    "change",

    async function (event) {

        if (

            !event.target.classList.contains(

                "script-file"

            )

        ) {

            return;

        }


        const file = event.target.files[0];


        if (!file) {

            return;

        }


        const nodeElement =

            event.target.closest(

                ".drawflow-node"

            );


        const nodeId = parseInt(

            nodeElement.id.replace(

                "node-",

                ""

            )

        );


        console.log(

            "Node ID:",

            nodeId

        );


        const scriptNameElement =

            event.target

                .closest(

                    ".script-node-content"

                )

                .querySelector(

                    ".script-name"

                );


        scriptNameElement.innerText =

            file.name;

        let node = editor.getNodeFromId(
            nodeId
        );
        const workflowName = document.querySelector("#Workflow_name").value;
        console.log(
            "Node:",
            node
        );

        if (node) {

            editor.drawflow.drawflow.Home.data[
                nodeId
            ].data.script_name =
                file.name;

        }

        console.log(
            editor.export()
        );

        let formData = new FormData();

        formData.append(
            "script",
            file
        );

        formData.append(
            "workflow_name",
            workflowName
        );

        formData.append(
            "node_id",
            nodeId
        );
        const response = await fetch(

            "/workflow/upload_script/",

            {

                method: "POST",

                headers: {

                    "X-CSRFToken":
                        getCookie(
                            "csrftoken"
                        )

                },

                body: formData

            }

        );


        const result =
            await response.json();

        console.log(
            result
        );


        if (node) {

            editor.drawflow.drawflow.Home.data[
                nodeId
            ].data.script_path =
                result.script_path;

        }

        console.log(
            editor.export()
        );

    }


);
document.addEventListener(

    "input",

    function (event) {

        if (

            !event.target.classList.contains(

                "node-input"

            )

        ) {

            return;

        }


        const nodeElement =

            event.target.closest(

                ".drawflow-node"

            );


        const nodeId = parseInt(

            nodeElement.id.replace(

                "node-",

                ""

            )

        );


        editor.drawflow.drawflow.Home.data[
            nodeId
        ].data.node_name =

            event.target.value;

    }

);
async function saveWorkflow() {

    let data = editor.export()
    const name = document.querySelector("#Workflow_name").value;
    console.log(data)

    await fetch(

        "/workflow/save/",

        {

            method: "POST",

            headers: {

                "Content-Type": "application/json",

                "X-CSRFToken": getCookie('csrftoken')

            },

            body: JSON.stringify(

                {

                    workflow_name: name,

                    description: "Created From Builder",

                    workflow: data

                }

            )

        }

    )

    alert(

        "Workflow Saved"

    )

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

        console.log("WorkflowID", this.dataset);

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

        console.log(result);

        // Restore button
        run_btn.innerHTML = "RUN";
        run_btn.style.backgroundColor = "";
        run_btn.disabled = false;

        alert("Workflow Execution Complete");

    });

});

document.querySelectorAll(".delete-btn").forEach(button => {

    button.addEventListener("click", async function () {

        console.log("WorkflowID", this.dataset)
        const workflowId = this.dataset.workflowId;


        const response = await fetch(
            `/workflow/delete/${workflowId}/`
        )

        const result = await response.json();

        console.log(result);

        // Update UI immediately
        alert("Workflow Deleted")
    });

});

function viewHistory(workflowId) {
    console.log(workflowId)

    window.location.href =

        `/workflowHistory/${workflowId}/`

}


async function deleteWorkflow(workflowId) {

    await fetch(

        `/workflow/delete/${workflowId}/`

    )

    loadWorkflows()

}




