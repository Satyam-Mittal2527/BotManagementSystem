from django.db import models
import mysql.connector
from datetime import datetime
import json
import mysql.connector
class WorkflowDatabaseModule:
    print("DATABASE MODULE LOADED")
    def __init__(self):
       pass
    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="1Satyam112@",
            database="sanima_bot"
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
    def save_workflow(self,workflow_name,description,workflow):
        workflow_id = self.insert_workflow(
            workflow_name,
            description
        )

        for node in workflow["nodes"]:

            self.insert_node(
                workflow_id,
                node
            )

        for edge in workflow["edges"]:

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