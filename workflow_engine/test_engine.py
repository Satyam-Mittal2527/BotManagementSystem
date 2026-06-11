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
            "type":"delay",
            "data":{
                "seconds":5
            }
        },

        {
            "id":"5",
            "type":"bot",
            "data":{
                "botId":9
            }
        },
        {
            "id":"6",
            "type":"api",
            "data":{
                "url":"https://jsonplaceholder.typicode.com/todos/1"
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
        },
        {
            "source":"3",
            "target":"4"
        },

        {
            "source":"4",
            "target":"5"
        },
        {
            "source":"5",
            "target":"6"
        }      

    ]

}

engine = WorkflowEngine()

engine.execute(workflow)