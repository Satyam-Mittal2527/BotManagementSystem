from django.db import models
import mysql.connector
from datetime import datetime
import json
import mysql.connector
class WorkflowDatabaseModule:
    # print("WORKFFLOW MODULE LOADED")
    def __init__(self):
       pass
    def get_connection(self):
        return mysql.connector.connect(
            host = os.getenv('DATABASE_HOST'),
            port = os.getenv('DATABASE_PORT'),
            user = os.getenv('DATABASE_USER'),
            password = os.getenv('DATABASE_PASSWORD'),
            database = os.getenv('DATABASE_NAME')
        )
    def insert_workflow(self, workflow_name, description):

        connection = self.get_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO WORKFLOWS(
                workflow_name,
                description
            )
            VALUES(%s,%s)
        """

        cursor.execute(
            query,
            (
                workflow_name,
                description
            )
        )

        connection.commit()

        workflow_id = cursor.lastrowid

        cursor.close()

        connection.close()

        return workflow_id

    def insert_node(self,workflow_id,node):

        connection = self.get_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO WORKFLOW_NODES(

            workflow_id,

            node_id,

            node_type,

            data_json

        )

        VALUES(%s,%s,%s,%s)

        """

        cursor.execute(

            query,

            (

                workflow_id,

                node["id"],

                node["type"],

                json.dumps(
                    node["data"]
                )

            )

        )

        connection.commit()

        cursor.close()

        connection.close()

    def insert_edge(self,workflow_id,edge):
        connection = self.get_connection()

        cursor = connection.cursor()

        query = """

        INSERT INTO WORKFLOW_EDGES(

            workflow_id,

            source_node,

            target_node,

            edge_label

        )

        VALUES(%s,%s,%s,%s)

            """

        cursor.execute(

            query,

            (

                workflow_id,

                edge["source"],

                edge["target"],

                    edge.get("label")

            )

        )

        connection.commit()

        cursor.close()

        connection.close()

    def get_workflow(self,workflow_id):

        connection = self.get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        # -----------------------
        # Load Nodes
        # -----------------------

        cursor.execute(

            """

            SELECT

            node_id,

            node_type,

            data_json

            FROM WORKFLOW_NODES

            WHERE workflow_id=%s

            """,

            (workflow_id,)

        )

        nodes_result = cursor.fetchall()
        # print("nodes_result =", nodes_result)

        nodes = []

        for node in nodes_result:

            nodes.append(

                {

                    "id": node["node_id"],

                    "type": node["node_type"],

                    "data": json.loads(
                        node["data_json"]
                    )

                }

            )

        # -----------------------
        # Load Edges
        # -----------------------

        cursor.execute(

            """

            SELECT

            source_node,

            target_node,

            edge_label

            FROM WORKFLOW_EDGES

            WHERE workflow_id=%s

            """,

            (workflow_id,)

        )

        edges_result = cursor.fetchall()

        edges = []

        for edge in edges_result:

            edge_dict = {

                "source": edge["source_node"],

                "target": edge["target_node"]

            }

            if edge["edge_label"]:

                edge_dict["label"] = edge["edge_label"]

            edges.append(
                edge_dict
            )

        cursor.close()

        connection.close()

        return {

            "nodes": nodes,

            "edges": edges

        }
    def save_workflow(self, workflow_name, description, workflow):

        workflow_id = self.insert_workflow(
            workflow_name,
            description
        )

        nodes = workflow["drawflow"]["Home"]["data"]

        for node_id, node in nodes.items():

            # Insert node
            self.insert_node(
                workflow_id,
                {
                    "id": node["id"],
                    "type": node["name"],
                    "data": node["data"]
                }
            )

            for output_name, output in node["outputs"].items():

                for connection in output["connections"]:

                    edge = {

                        "source": node["id"],

                        "target": int(
                            connection["node"]
                        )

                    }

                    # Decision node
                    if node["name"] == "decision":

                        if output_name == "output_1":

                            edge["label"] = "True"

                        elif output_name == "output_2":

                            edge["label"] = "False"

                    self.insert_edge(

                        workflow_id,

                        edge

        )

        return workflow_id
    def insert_workflow_run(self,workflow_id):
        connection = self.get_connection()

        cursor = connection.cursor()

        query = """

        INSERT INTO WORKFLOW_RUNS(

            workflow_id,

            status,

            started_at

        )

        VALUES(

            %s,

            %s,

            NOW()

        )

        """

        cursor.execute(

            query,

            (

                workflow_id,

                "RUNNING"

            )

        )

        connection.commit()

        run_id = cursor.lastrowid

        cursor.close()

        connection.close()

        return run_id
    def update_workflow_run(self,run_id,status):

        connection = self.get_connection()

        cursor = connection.cursor()

        query = """

        UPDATE WORKFLOW_RUNS

        SET

        status=%s,

        ended_at=NOW()

        WHERE id=%s

        """

        cursor.execute(

            query,

            (

                status,

                run_id

            )

        )

        connection.commit()

        cursor.close()

        connection.close()
    def insert_node_run(self,workflow_run_id,node_id,node_type,status,message):

        connection = self.get_connection()

        cursor = connection.cursor()

        query = """

        INSERT INTO WORKFLOW_NODE_RUNS(

            workflow_run_id,

            node_id,

            node_type,

            status,

            message

        )

        VALUES(

            %s,

            %s,

            %s,

            %s,

            %s

        )

        """

        cursor.execute(

            query,

            (

                workflow_run_id,

                node_id,

                node_type,

                status,

                message

            )

        )

        connection.commit()

        cursor.close()

        connection.close()
    def get_workflow_runs(self,workflow_id):
        conn = self.get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        sql = """
        SELECT *
        FROM WORKFLOW_RUNS
        WHERE workflow_id=%s
        ORDER BY id DESC
        """

        cursor.execute(
            sql,
            (
                workflow_id,
            )
        )

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows


    def get_node_runs(
    self,
    workflow_id
):

        conn = self.get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        sql = """

        SELECT N.*

        FROM WORKFLOW_NODE_RUNS N

        JOIN WORKFLOW_RUNS W

        ON N.workflow_run_id=W.id

        WHERE W.workflow_id=%s

        ORDER BY N.id DESC

        """

        cursor.execute(
            sql,
            (
                workflow_id,
            )
        )

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows
    def get_all_workflows(self):

        conn = self.get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        sql = """
        SELECT *
        FROM WORKFLOWS
        ORDER BY id DESC
        """

        cursor.execute(sql)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows
    def get_dashboard(self):

        conn = self.get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        dashboard = {}

        # Total workflows

        cursor.execute(
            """
            SELECT COUNT(*) total
            FROM WORKFLOWS
            """
        )

        dashboard["total_workflows"] = cursor.fetchone()["total"]


        # Running workflows

        cursor.execute(
            """
            SELECT COUNT(*) total
            FROM WORKFLOW_RUNS
            WHERE status='RUNNING'
            """
        )

        dashboard["running"] = cursor.fetchone()["total"]


        # Completed workflows

        cursor.execute(
            """
            SELECT COUNT(*) total
            FROM WORKFLOW_RUNS
            WHERE status='COMPLETED'
            """
        )

        dashboard["completed"] = cursor.fetchone()["total"]


        # Failed workflows

        cursor.execute(
            """
            SELECT COUNT(*) total
            FROM WORKFLOW_RUNS
            WHERE status='FAILED'
            """
        )

        dashboard["failed"] = cursor.fetchone()["total"]

        cursor.close()
        conn.close()

        return dashboard
    def delete_workflow(self, workflowId):
        conn = self.get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        sql = """
            DELETE FROM WORKFLOWS WHERE 
            id = %s
        """
        try:
            cursor.execute(sql, (workflowId,))
            conn.commit()

            return {
                "Deleted Logs"
            }
        except Exception as e:
            # print(str(e))
            return str(e)
        finally:
            cursor.close()
            conn.close()
    def insert_log(

        self,

        workflow_run_id,

        node_id,

        log_level,

        message

    ):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute(

            """

            INSERT INTO WORKFLOW_LOGS(

                workflow_run_id,

                node_id,

                log_level,

                message

            )

            VALUES(%s,%s,%s,%s)

            """,

            (

                workflow_run_id,

                node_id,

                log_level,

                message

            )

        )

        connection.commit()

        cursor.close()

        connection.close()

    def get_logs(

        self,

        workflow_run_id

    ):

        connection = self.get_connection()

        cursor = connection.cursor(

            dictionary=True

        )

        cursor.execute(

            """

            SELECT *

            FROM WORKFLOW_LOGS

            WHERE workflow_run_id=%s

            ORDER BY created_at

            """,

            (workflow_run_id,)

        )

        logs = cursor.fetchall()

        cursor.close()

        connection.close()

        return logs

    def get_workflow_by_id(

        self,

        workflow_id

    ):

        conn = self.get_connection()

        cursor = conn.cursor(

            dictionary=True

        )

        cursor.execute(

            """

            SELECT *

            FROM WORKFLOWS

            WHERE id=%s

            """,

            (

                workflow_id,

            )

        )

        workflow = cursor.fetchone()

        cursor.close()

        conn.close()

        return workflow