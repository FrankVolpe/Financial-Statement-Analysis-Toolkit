import sqlite3
import pandas as pd

path = '/media/francesco/hdd/data/'
file_end = '.sqlite'



def save_from_pandas(name_of_table, db_name, df, if_exists='replace'):
    ## Route to database
    connection = sqlite3.connect(path + db_name + file_end)
    df.to_sql(name_of_table, connection, if_exists=if_exists)


## PANDAS FUNCTION USED BELOW DOESNT SUPPORT SQLITE CONNECTION
## OBJECTS SO I HAVE TO CONVERT TO SQLALCHEMY

#def load_to_pandas(name_of_table):
#    return pd.read_sql_table(name_of_table)
