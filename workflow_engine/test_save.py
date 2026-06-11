from modules.workflow_database_module import WorkflowDatabaseModule

database = WorkflowDatabaseModule()

workflow = {

    "nodes":[

        {
            "id":"1",
            "type":"variable",
            "data":{
                "name":"amount",
                "value":5000
            }
        },

        {
            "id":"2",
            "type":"bot",
            "data":{
                "botId":7
            }
        }

    ],

    "edges":[

        {
            "source":"1",
            "target":"2"
        }

    ]

}

workflow_id = database.save_workflow(

    "Transaction Workflow",

    "Testing",

    workflow

)

print(workflow_id)