import psycopg2
from os import environ
from dotenv import load_dotenv


class DB_Test_Postgres:
    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self):
        self.conn = psycopg2.connect(
            host=environ.get('TEST_SERVER'), port=environ.get('TEST_PORT'), user=environ.get('TEST_USERNAME'), password=environ.get('TEST_PASSWORD'), database=environ.get('TEST_DATABASE'))
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.close()



