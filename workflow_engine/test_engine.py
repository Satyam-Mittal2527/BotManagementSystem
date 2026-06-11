from workflow_engine.engine import WorkflowEngine

workflow = {

    "nodes":[

        {
            "id":"1",
            "type":"variable",
            "data":{
                "name":"amount",
                "value":500
            }
        },

        {
            "id":"2",
            "type":"condition",
            "data":{
                "code":"amount > 1000"
            }
        },

        {
            "id":"3",
            "type":"bot",
            "data":{
                "botId":7
            }
        },

        {
            "id":"4",
            "type":"bot",
            "data":{
                "botId":9
            }
        }

    ],

    "edges":[

        {
            "source":"1",
            "target":"2"
        },

        {
            "source":"2",
            "target":"3",
            "label":"True"
        },

        {
            "source":"2",
            "target":"4",
            "label":"False"
        }

    ]

}

engine = WorkflowEngine()

engine.execute(workflow)