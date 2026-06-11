from modules.workflow_database_module import WorkflowDatabaseModule
from workflow_engine.engine import WorkflowEngine

database = WorkflowDatabaseModule()

workflow = database.get_workflow(6)


print(workflow)

engine = WorkflowEngine()

engine.execute(
    workflow,
    6
)  
