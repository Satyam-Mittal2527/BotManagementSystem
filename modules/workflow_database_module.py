from django.db import models
import mysql.connector
from datetime import datetime

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

    def insert_node(self):
        pass

    def insert_edge(self):
        pass

    def get_workflow(self):
        pass