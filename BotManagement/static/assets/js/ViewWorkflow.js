document.querySelectorAll(".file-btn")
    .forEach(button => {

        button.addEventListener(
            "click",
            async function () {

                const file =
                    this.dataset.file;

                const workflowName =
                    document.getElementById(
                        "BotName"
                    ).value;

                const response =
                    await fetch(

                        "/workflow/open_file/",

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
                                        workflowName,

                                    file_path:
                                        file

                                }

                            )

                        }

                    );

                const result =
                    await response.json();

                document.getElementById(
                    "BotCode"
                ).value =
                    result.code;

            }

        );

    });
document
    .getElementById(
        "EditBotForm"
    )
    .addEventListener(
        "submit",
        async function (e) {

            e.preventDefault();

            const workflowName =
                document
                    .getElementById(
                        "BotName"
                    )
                    .value;

            const currentFile =
                document
                    .getElementById(
                        "CurrentFile"
                    )
                    .value;

            const code =
                document
                    .getElementById(
                        "BotCode"
                    )
                    .value;

            const response =
                await fetch(

                    "/workflow/edit_file/",

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
                                    workflowName,

                                file_path:
                                    currentFile,

                                code:
                                    code

                            }

                        )

                    }

                );

            const result =
                await response.json();

            alert(
                result.message
            );

        }

    );