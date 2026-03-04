from mysql.connector import connect
class Database:
    def __init__(self,host,user,password,database):
        self.connectionObj = {"host":host,"user":user,"password":password,"database":database}
    def CreateConnection(self):
        return connect(**self.connectionObj)
    def GetData(self,sqlquery,fetchType = "one" or "many"):
        conn = self.CreateConnection()
        cursor = conn.cursor()
        cursor.execute(sqlquery)
        data = cursor.fetchall() if fetchType == "many" else cursor.fetchone()
        return data
        pass
    def InsertData(self,sqlquery,values):
        try:
            conn = self.CreateConnection()
            cursor = conn.cursor()
            cursor.executemany(sqlquery,values)
            conn.commit()
            return "success"
        except Exception as err:
            raise "error"
        pass
