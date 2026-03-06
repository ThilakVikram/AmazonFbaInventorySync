from Tablequery import TableQuery
from Database import Database
from SPAPI_Caller import Values_Getter,Region,NA_Marketplace,EU_Marketplace,FE_Marketplace

if __name__ == "__main__":
    available_marketplace = {Region.EU:[EU_Marketplace.UK,EU_Marketplace.DE,EU_Marketplace.FR,EU_Marketplace.SA,EU_Marketplace.NL,EU_Marketplace.PL,EU_Marketplace.ES,EU_Marketplace.AE],Region.FE:[FE_Marketplace.JP]}
    for region in available_marketplace.keys():
        for marketplace in available_marketplace.get(region):
            for values in Values_Getter(region,marketplace):
                # print(values)
                print(Database(host="localhost",user="root",password="admin",database="itrend").InsertData(TableQuery().getContent("warehouse_stock","insert"),values))
    pass