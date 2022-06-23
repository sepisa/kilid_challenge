#### database.py

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd


class Database:

    def __init__(self, host='localhost', port=5432, user='postgres'):
        self.host = host
        self.port = port
        self.user = user
        self.conn = None
        self.cursor = None
        self.connect_to_database()
    #create local database
    def create_database(self):
        conn = psycopg2.connect(host=self.host, port=self.port, user=self.user)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE kilid")
        return

    #set connection to database
    def connect_to_database(self, db='kilid'):
        self.conn = psycopg2.connect(host=self.host, port=self.port, user=self.user, database='kilid')
        self.cursor = self.conn.cursor()
        return

    #create table in database
    def create_table(self):
        self.cursor.execute(
            "CREATE TABLE CURRENCY(ID SERIAL PRIMARY KEY, START real, MIN real, MAX real, END2 real, CHANGE real, "
            "PERCENTAGE_CHANGE FLOAT, GR_DATE DATE)")
        self.conn.commit()
        return

    #i nsert the crawl data to CURRENCY table
    def insert(self, *args):
        self.cursor.execute("""INSERT INTO CURRENCY (START, MIN, MAX, END2, CHANGE, PERCENTAGE_CHANGE, GR_DATE) 
        VALUES(%s, %s, %s, %s, %s, %s, %s)""", args)
        self.conn.commit()
        return

    # Read data from CURRENCY
    def read_table(self):
        self.cursor.execute("""select * from CURRENCY""")
        records = self.cursor.fetchall()
        # row_count = 2
        # records = self.cursor.fetchmany(row_count)
        df = pd.DataFrame(records, columns=['id','OPEN', 'MIN', 'MAX', 'CLOSE', 'CHANGE', 'PERCENTAGE_CHANGE', 'GR_DATE'])
        return df
