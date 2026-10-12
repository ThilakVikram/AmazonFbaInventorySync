from requests import get
from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from .Tablequery import TableQuery
from .Database import Database
from .SPAPI_Caller import Values_Getter,Region,NA_Marketplace,EU_Marketplace,FE_Marketplace
from datetime import datetime

path = Path(__file__).resolve().parent / ".env"
print(path)
load_dotenv(path)


def main():
    print(datetime.now())
    available_marketplace = {Region.NA:[NA_Marketplace.US,NA_Marketplace.CA,NA_Marketplace.MX],Region.EU:[EU_Marketplace.UK,EU_Marketplace.DE,EU_Marketplace.FR,EU_Marketplace.SA,EU_Marketplace.NL,EU_Marketplace.PL,EU_Marketplace.ES,EU_Marketplace.AE],Region.FE:[FE_Marketplace.JP]}
    for region in available_marketplace.keys():
        for marketplace in available_marketplace.get(region):
            print(region)
            # get(getenv("notification_url")+"?wname="+"FBA "+region.value+"Script&status=success&detail=completed successfully")
            for values in Values_Getter(region,marketplace):
                # print(values)
                # print(values[0])
                Database().InsertData(TableQuery().getContent("warehouse_stock","insert"),values)
    pass
