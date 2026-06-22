# SANIMA - Bot Management System

A Django-based automation platform developed during the internship at **Sanima Bank**. The project provides two major modules:

* **Bot Management System**
* **Workflow Builder and Execution Engine**

---

# Features

## Bot Management

* Create and register bots
* Upload Python bot folders
* Start bots
* Stop bots
* Monitor bot status
* Store process IDs
* Real-time logging
* Execution history
* Export logs to Excel
* Delete bots
* Archive deleted bots

---

## Workflow Builder

* Drag-and-drop workflow design
* Start Node
* Process Node
* Condition Node
* Loop Node
* End Node

---

## Workflow Engine

* Graph-based execution
* Shared runtime context
* Variable passing between nodes
* Sequential execution
* Conditional branching
* Execution history
* Node-level logs

---

## Workflow File Explorer

* View workflow files
* Edit node scripts
* Dynamic file loading
* Save modifications directly to disk

---

# Tech Stack

### Backend

* Python
* Django

### Database

* SQLite
* MySQL

### Frontend

* HTML
* CSS
* Bootstrap
* JavaScript

### Workflow Builder

* Drawflow

---

# Project Structure

```text
SANIMABA
│
├── bot/
│   ├── __init__.py
│   └── bank_bot.py
│
├── BotManagement/
│   ├── static/
│   ├── templates/
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   └── admin.py
│
├── WorkflowManagement/
│   ├── workflow/
│   │
│   ├── workflow_engine/
│   │   ├── engine.py
│   │   ├── registry.py
│   │   └── nodes/
│   │       ├── script_node.py
│   │       ├── condition_node.py
│   │       ├── loop_node.py
│   │       ├── end_node.py
│   │       └── ...
│   │
│   ├── views.py
│   └── urls.py
│
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# Workflow Storage

```text
WorkflowStorage/

workflow_TestWorkflow/

    node_1/
        main.py

    node_2/
        main.py

    node_3/
        main.py
```

---

# Deleted Workflow Storage

```text
DeletedWorkflowFolder/

workflow_TestWorkflow/
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd SANIMABA
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Server

```bash
python manage.py runserver
```

---

# Future Improvements

* API Nodes
* Delay Nodes
* Email Nodes
* Scheduler Support
* Parallel Execution
* Docker Support
* Webhooks
* Multi-user support
* Authentication and Authorization
* Restore Deleted Workflows
* Role-Based Access Control

---

# Author

**Satyam Mittal**
www.linkedin.com/in/satyam-mittal2527

# SANIMABA - Bot Management and Workflow Automation Platform

A Django-based automation platform developed during the internship at **Sanima Bank**. The project provides two major modules:

* **Bot Management System**
* **Workflow Builder and Execution Engine**

---

# Features

## Bot Management

* Create and register bots
* Upload Python bot folders
* Start bots
* Stop bots
* Monitor bot status
* Store process IDs
* Real-time logging
* Execution history
* Export logs to Excel
* Delete bots
* Archive deleted bots

---

## Workflow Builder

* Drag-and-drop workflow design
* Start Node
* Process Node
* Condition Node
* Loop Node
* End Node

---

## Workflow Engine

* Graph-based execution
* Shared runtime context
* Variable passing between nodes
* Sequential execution
* Conditional branching
* Execution history
* Node-level logs

---

## Workflow File Explorer

* View workflow files
* Edit node scripts
* Dynamic file loading
* Save modifications directly to disk

---

# Tech Stack

### Backend

* Python
* Django

### Database

* SQLite
* MySQL

### Frontend

* HTML
* CSS
* Bootstrap
* JavaScript

### Workflow Builder

* Drawflow

---

# Project Structure

```text
SANIMABA
│
├── bot/
│   ├── __init__.py
│   └── bank_bot.py
│
├── BotManagement/
│   ├── static/
│   ├── templates/
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   └── admin.py
│
├── WorkflowManagement/
│   ├── workflow/
│   │
│   ├── workflow_engine/
│   │   ├── engine.py
│   │   ├── registry.py
│   │   └── nodes/
│   │       ├── script_node.py
│   │       ├── condition_node.py
│   │       ├── loop_node.py
│   │       ├── end_node.py
│   │       └── ...
│   │
│   ├── views.py
│   └── urls.py
│
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# Workflow Storage

```text
WorkflowStorage/

workflow_TestWorkflow/

    node_1/
        main.py

    node_2/
        main.py

    node_3/
        main.py
```

---

# Deleted Workflow Storage

```text
DeletedWorkflowFolder/

workflow_TestWorkflow/
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd SANIMABA
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Server

```bash
python manage.py runserver
```

---

# Author

**Satyam Mittal**
www.linkedin.com/in/satyam-mittal2527
