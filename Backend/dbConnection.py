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

    def delete_flake(
        self,
        _id,
    ):
        query = """
        SELECT flake.id, flake.size,flake.thickness,flake.used,c.material FROM flake
        JOIN chip c on c.id = flake.chip_id
        JOIN scan s on s.id = c.scan_id
        LIMIT %s;
        """

        self.cur.execute(query, (flake_limit,))
        # gets the last image_id
        flake_dict = self.cur.fetchall()
        # makes sure the databank is consistent
        self.conn.commit()

        return flake_dict

    def build_query(self, flake_limit, minSize, material, thickness):
        """
        Builds a query from the given query params
        """

        # Default Query
        query = """
        SELECT flake.id, flake.size,flake.thickness,flake.used,c.material FROM flake
        JOIN chip c on c.id = flake.chip_id
        JOIN scan s on s.id = c.scan_id
        WHERE size > {}\n""".format(
            float(minSize)
        )

        if material is not None:
            query += """AND material = '{}'\n""".format(material)

        if thickness is not None:
            query += """AND thickness = {}\n""".format(int(thickness))

        query += """ORDER BY flake.size DESC\n"""
        query += """LIMIT {}""".format(int(flake_limit))
        return query

    def get_flakes(
        self,
        flake_limit=100,
        minSize=0,
        material=None,
        thickness=None,
        **kwargs,
    ):
        query = self.build_query(flake_limit, minSize, material, thickness)

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
