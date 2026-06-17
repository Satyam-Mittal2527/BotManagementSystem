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
let currentNode = null;
let codeEditor = null;
document.addEventListener("DOMContentLoaded", function () {

    document
        .getElementById(
            "editorModal"
        )
        .addEventListener(

            "shown.bs.modal",

            function () {

                largeEditor.setValue(

                    codeEditor.getValue()

                );

                largeEditor.layout();

            }

        );


    document
        .getElementById(
            "editorModal"
        )
        .addEventListener(

            "hidden.bs.modal",

            function () {

                codeEditor.setValue(

                    largeEditor.getValue()

                );

            }

        );
    const drawflow = document.getElementById("drawflow");

    // console.log("drawflow =", drawflow);

    editor = new Drawflow(drawflow);

    editor.start();

    require.config({

        paths: {

            vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs'

        }

    });

    require(

        ['vs/editor/editor.main'],

        function () {

            codeEditor = monaco.editor.create(

                document.getElementById(
                    'monaco-editor'
                ),

                {

                    value: '',

                    language: 'python',

                    theme: 'vs-dark',

                    automaticLayout: true,

                    minimap: {

                        enabled: false

                    }

                }

            );
            largeEditor = monaco.editor.create(

                document.getElementById(

                    "monaco-editor-large"

                ),

                {

                    value: "",

                    language: "python",

                    theme: "vs-dark",

                    automaticLayout: true

                }

            );

            codeEditor.layout({
                width: 250,
                height: 250
            });



        }

    );
    editor.on("nodeSelected", function (id) {

        currentNode = id;

        document
            .getElementById(
                "properties-panel"
            )
            .classList.add(
                "active"
            );

        let node =
            editor.drawflow.drawflow.Home.data[id];

        document
            .getElementById(
                "property_node_name"
            )
            .value =
            node.data.node_name || "";

        document
            .getElementById(
                "script-language"
            )
            .value =
            node.data.language || "python";

        if (codeEditor) {

            codeEditor.setValue(

                node.data.script_content || ""

            );

        }

    });

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
    // console.log("Dropped")

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

    const rect =
        editor.precanvas.getBoundingClientRect();

    pos_x -= rect.x;
    pos_y -= rect.y;

    let html = "";

    switch (name) {

        case "process":

            html = `
            <div class="process-node">
                <h5>Process</h5>
            </div>
            `;

            break;


        case "decision":

            html = `
            <div class="decision-node">
                Decision
            </div>
            `;


            break;


        case "start":

            html = `
            <div class="start-node">
                Start
            </div>
            `;

            break;
        case "loop":

            html = `
        <div class="loop-node">
            <i class="bi bi-arrow-repeat"></i>
        </div>
    `;

            break;
        case "end":

            html = `
        <div class="end-node">
            End
        </div>
    `;

            break;

        default:

            html = `
            <div class="script-node-content">
                <h5>Script Node</h5>
            </div>
            `;
    }


    if (name == "decision" || name == "loop") {

        editor.addNode(

            name,

            1,

            2,

            pos_x,

            pos_y,

            name,

            {
                node_name: "",
                script_content: "",
                script_path: "",
                language: "python"
            },

            html,

            false

        );

    }
    else if (name == "end") {

        editor.addNode(

            name,

            1,

            0,

            pos_x,

            pos_y,

            name,

            {
                node_name: "",
                script_content: "",
                script_path: "",
                language: "python"
            },

            html,

            false

        );

    }
    else {

        editor.addNode(

            name,

            1,

            1,

            pos_x,

            pos_y,

            name,

            {
                node_name: "",
                script_content: "",
                script_path: "",
                language: "python"
            },

            html,

            false

        );

    }

}
document
    .getElementById("script-language")
    .addEventListener(

        "change",

        function () {

            if (codeEditor) {

                monaco.editor.setModelLanguage(

                    codeEditor.getModel(),

                    this.value

                );

            }

            if (currentNode) {

                editor.drawflow.drawflow.Home.data[
                    currentNode
                ].data.language =
                    this.value;

            }

        }

    );
document
    .getElementById("property_script")
    .addEventListener(
        "change",
        async function () {

            if (!currentNode)
                return;

            const workflowName =
                document.querySelector(
                    "#Workflow_name"
                ).value.trim();

            if (!workflowName) {

                alert(
                    "Please enter a workflow name first."
                );

                this.value = "";

                return;
            }

            const file = this.files[0];

            if (!file)
                return;

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
                currentNode
            );

            let node =
                editor.getNodeFromId(
                    currentNode
                );

            node.data.script_name =
                file.name;

            node.data.script_path =
                result.script_path;
        }
    );
async function saveWorkflow() {

    const name =
        document
            .querySelector(
                "#Workflow_name"
            )
            .value
            .trim();

    if (!name) {

        alert(
            "Please enter a Workflow Name."
        );

        return;
    }

    const workflow =
        editor.export();

    const nodes =
        Object.values(
            workflow.drawflow.Home.data
        );

    // Check Start Node
    const startNodes =
        nodes.filter(
            node =>
                node.name === "start"
        );

    if (startNodes.length === 0) {

        alert(
            "Workflow must contain one Start Node."
        );

        return;
    }

    if (startNodes.length > 1) {

        alert(
            "Workflow cannot contain more than one Start Node."
        );

        return;
    }

    // Check End Node
    const endNodes =
        nodes.filter(
            node =>
                node.name === "end"
        );

    if (endNodes.length === 0) {

        alert(
            "Workflow must contain one End Node."
        );

        return;
    }

    console.log(
        workflow
    );

    const response =
        await fetch(

            "/workflow/save/",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json",

                    "X-CSRFToken":
                        getCookie(
                            "csrftoken"
                        )

                },

                body: JSON.stringify(

                    {

                        workflow_name:
                            name,

                        description:
                            "Created From Builder",

                        workflow:
                            workflow

                    }

                )

            }

        );

    const result =
        await response.json();

    if (
        result.status ===
        "success"
    ) {

        alert(
            "Workflow Saved Successfully"
        );

    }

    else {

        alert(
            result.message
        );

    }

}
document
    .getElementById("saveNode")
    .addEventListener("click", function () {

        if (currentNode == null)
            return;

        const workflowName =
            document
                .getElementById(
                    "Workflow_name"
                )
                .value
                .trim();

        if (!workflowName) {

            alert(
                "Please enter a Workflow Name before saving nodes."
            );

            document
                .getElementById(
                    "Workflow_name"
                )
                .focus();

            return;
        }

        let node =
            editor.drawflow.drawflow.Home.data[
            currentNode
            ];

        node.data.node_name =
            document
                .getElementById(
                    "property_node_name"
                )
                .value;

        node.data.language =
            document
                .getElementById(
                    "script-language"
                )
                .value;

        if (codeEditor) {

            node.data.script_content =
                codeEditor.getValue();

        }

        const titleElement =
            document.querySelector(
                `#node-${currentNode} h5`
            );

        if (titleElement) {

            titleElement.innerText =
                node.data.node_name ||
                "Script Node";

        }

        alert(
            "Node saved successfully!"
        );

    });