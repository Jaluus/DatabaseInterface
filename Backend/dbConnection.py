import numpy as np
import mysql.connector
from config import config
import sys
import os
import time


class dbConnectionQuery:
    def __init__(self):
        try:
            self.params = config()

            # connect to the MySQL server
            print("Connecting to the MySQL database...")
            self.conn = mysql.connector.connect(**self.params)

            # create a cursor
            self.cur = self.conn.cursor(dictionary=True)
        except (Exception) as error:
            print(error)
            sys.exit(0)

    def build_query(
        self,
        minSize=0,
        exfoliated_material=None,
        thickness=None,
        flake_limit=100,
        **kwargs,
    ):
        """
        Builds a query from the given query params
        """

        # Default Query; Where 1=1 is a Workaround to make it easier to add multiple and clauses
        query = """
        SELECT flake.id, flake.size,flake.thickness,flake.used,c.exfoliated_material FROM flake
        JOIN chip c on c.id = flake.chip_id
        JOIN scan s on s.id = c.scan_id
        WHERE 1=1\n"""

        if minSize is not None:
            query += """AND size > {}\n""".format(float(minSize))

        if exfoliated_material is not None:
            query += """AND exfoliated_material = '{}'\n""".format(exfoliated_material)

        if thickness is not None:
            query += """AND thickness = '{}'\n""".format(thickness)

        # query += """ORDER BY flake.size DESC\n"""
        query += """LIMIT {}""".format(int(flake_limit))
        return query

    def get_flakes(
        self,
        query_dict,
    ):
        query = self.build_query(**query_dict)

        print(query)

        self.cur.execute(query)
        # gets the last image_id
        flake_dict = self.cur.fetchall()
        # makes sure the databank is consistent
        self.conn.commit()

        return flake_dict

    def __delete__(self):
        if self.conn is not None:
            self.conn.close()
            print("Database connection closed.")
