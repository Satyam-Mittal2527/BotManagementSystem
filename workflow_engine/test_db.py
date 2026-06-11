from modules.workflow_database_module import WorkflowDatabaseModule

database = WorkflowDatabaseModule()

workflow_id = database.insert_workflow(
    "Transaction Workflow",
    "Testing workflow"
)

print(workflow_id)