from modules.workflow_database_module import WorkflowDatabaseModule

database = WorkflowDatabaseModule()

workflow_id = database.insert_workflow(
    "Transaction Workflow",
    "Testing workflow"
)

database.insert_node(

    workflow_id,

    {

        "id":"1",

        "type":"variable",

        "data":{

            "name":"amount",

            "value":5000

        }

    }

)

database.insert_node(

    workflow_id,

    {

        "id":"2",

        "type":"bot",

        "data":{

            "botId":7

        }

    }

)

database.insert_edge(

    workflow_id,

    {

        "source":"1",

        "target":"2"

    }

)

print(workflow_id)