from os import getenv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")
from mysql.connector import connect
class Database:
    def __init__(self):
        self.connectionObj = {"host":getenv("host"),"user":getenv("user"),"password":getenv("password"),"database":getenv("database")}
    def CreateConnection(self):
        return connect(**self.connectionObj)
    def GetData(self,sqlquery,fetchType = "one" or "many"):
        try:
            conn = self.CreateConnection()
            cursor = conn.cursor()
            cursor.execute(sqlquery)
            data = cursor.fetchall() if fetchType == "many" else cursor.fetchone()
            return data
        finally:
            conn.close()
        pass
    def InsertData(self,sqlquery,values):
        conn = self.CreateConnection()
        try:
            cursor = conn.cursor()
            cursor.executemany(sqlquery,values)
            conn.commit()
            # print("Inserted Success")
            return "success"
        except Exception as err:
            raise Exception(err)
        finally:
            conn.close()
        pass
