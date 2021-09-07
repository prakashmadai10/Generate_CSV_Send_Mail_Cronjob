import pandas as pd
import numpy as np
from datetime import datetime
from DB_CONNECT.connect import DB_Test_Postgres



def extract_data_db_dataframe():
    db = DB_Test_Postgres()
    sql = """Select * from mantis """
    db.connect()
    df = pd.read_sql(sql, db.conn)

    db.close()
    return df


