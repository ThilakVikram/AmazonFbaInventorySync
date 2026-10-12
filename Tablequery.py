from pathlib import Path
baseUrl = Path(__file__).resolve().parent
class TableQuery():
    def __init__(self):
        self.baseUrl = baseUrl
    def getContent(self,tableName,actionType):
        try:
            with open(self.baseUrl/"query"/tableName/(actionType+".sql"),"r") as file:
                return file.read()
        except Exception as err:
            raise Exception(err)