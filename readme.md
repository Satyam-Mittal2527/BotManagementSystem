# Workflow Management System

A Django-based workflow automation platform inspired by tools like n8n and Node-RED. Users can visually create workflows, attach Python scripts to nodes, execute workflows, monitor execution history, and manage workflow files through an integrated editor.

---

## Features

* Visual workflow builder
* Start, Process, Condition, Loop and End nodes
* Python script execution inside nodes
* Shared context between nodes
* Workflow execution history
* Node execution logs
* File explorer for workflow scripts
* Edit workflow scripts directly from UI
* Archive deleted workflows
* Workflow persistence in MySQL
* Folder-based code storage
* Dynamic workflow execution engine

---

## Architecture

### Workflow Metadata

Stored in MySQL:

* Workflow name
* Nodes
* Edges
* Node types
* Script paths

### Workflow Code

Stored in the file system:

```text
WorkflowStorage/
└── workflow_MyWorkflow
    ├── node_1
    │   └── main.py
    ├── node_2
    │   └── main.py
    └── node_3
        └── main.py
```

### Runtime Context

Variables are shared between nodes through a common execution context:

```python
name = "Satyam"

# Node 2
print(name)
```

---

## Tech Stack

### Backend

* Python
* Django
* MySQL

### Frontend

* HTML
* CSS
* JavaScript
* Bootstrap
* Drawflow

---

## Project Structure

```text
WorkflowManagement/
│
├── workflow/
│
├── workflow_engine/
│   ├── engine.py
│   ├── registry.py
│   └── nodes/
│       ├── script_node.py
│       ├── condition_node.py
│       ├── loop_node.py
│       └── end_node.py
│
├── templates/
├── static/
├── views.py
├── urls.py
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd <project-folder>
```

---

### Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Database

Update `settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "your_database",
        "USER": "your_username",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "3306"
    }
}
```

---

## Configure Storage Paths

In `settings.py`:

```python
WORKFLOW_STORAGE_PATH = "/path/to/WorkflowStorage"

DELETED_WORKFLOW_PATH = "/path/to/DeletedWorkflowFolder"
```

---

## Run Migrations

```bash
python manage.py migrate
```

---

## Start Server

```bash
python manage.py runserver
```

---

## Workflow Execution Flow

```text
Start Node
      ↓
Process Node
      ↓
Condition Node
   ↙        ↘
True       False
 ↓            ↓
Process     Process
      ↓
End Node
```

---

## Editing Workflow Files

Scripts are stored inside:

```text
WorkflowStorage/
```

Example:

```text
workflow_TestWorkflow/
    node_1/main.py
    node_2/main.py
    node_3/main.py
```

The workflow engine always executes the latest file contents.

---

## Deleting Workflows

Deleted workflows are moved to:

```text
DeletedWorkflowFolder/
```

instead of being permanently removed.

---

## Future Improvements

* Drag and drop workflow builder
* API nodes
* Delay nodes
* Parallel execution
* Scheduler support
* Cron jobs
* Variable nodes
* Email nodes
* Webhook nodes
* Restore deleted workflows
* Docker deployment
* Multi-user support
* Role-based access control

---

## Author

**Satyam Mittal**

