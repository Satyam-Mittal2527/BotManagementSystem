from modules.workflow_database_module import WorkflowDatabaseModule
from workflow_engine.engine import WorkflowEngine

database = WorkflowDatabaseModule()

workflow = database.get_workflow(5)    # use the workflow ID printed by test_db.py

print(workflow)

engine = WorkflowEngine()

engine.execute(workflow)