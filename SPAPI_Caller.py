import time
from .Tablequery import TableQuery
from .Database import Database
import pandas as pd
import datetime
from typing import Union
from .SPAPI_Container import SPAPI_Container,Region,NA_Marketplace,EU_Marketplace,FE_Marketplace
import requests


class SPAPI_Caller(SPAPI_Container):
    def __init__(self,region:Region):
        self.region = region.value
        self.access_token = self.generateAccessToken()
        print("Stored Access Token")
        
    def generateAccessToken(self):
        config = {
            "url" : f"https://api.amazon.com/auth/o2/token?grant_type=refresh_token&refresh_token={self.refresh_token_map.get(self.region)}&client_id={self.client_id}&client_secret={self.client_secret}",
            "headers" : {
                "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8"
        }}
        response = requests.post(**config)
        # print("Requested for Access Token")
        return response.json().get("access_token")
        pass
    def getInventorySummary(self,marketplace:Union[NA_Marketplace,EU_Marketplace,FE_Marketplace],nextToken = None):
        nextToken = nextToken
        self.marketplaceID = self.marketplace_id_map.get("region").get(self.region).get(marketplace.value)
        while nextToken != "":
            if self.access_token != None:
                url = f"https://sellingpartnerapi-{self.region}.amazon.com/fba/inventory/v1/summaries?details=true&granularityType=Marketplace&granularityId={self.marketplaceID}&marketplaceIds={self.marketplaceID}&nextToken={nextToken if nextToken else ""}"+""
                # print("url : "+url+" nextToken : "+nextToken if nextToken else "")
                headers = {
                    "x-amz-access-token":self.access_token
                }
                try:
                    response = requests.get(url,headers=headers,timeout=10)
                    data = response.json()
                    # print(response.status_code)
                    # print(data)
                    match response.status_code:
                        case 200:
                            try:
                                nextToken = data.get("pagination").get("nextToken")
                                # print("Next Token" + nextToken)
                                pass
                            except Exception as e:
                                nextToken = ""
                                # print("No More Pagination")
                            yield data.get("payload").get("inventorySummaries")
                        case 403:
                            self.generateAccessToken()
                            self.getInventorySummary(marketplace,nextToken)
                        case 400:
                            raise Exception("Missing Required Details")
                        case 429:
                            time.sleep(3)
                            self.getInventorySummary(marketplace,nextToken)
                            pass
                        case _:
                            raise Exception("Error Occured with Status "+response.status_code)
                except Exception as e:
                    print(e)
                    self.getInventorySummary(marketplace,nextToken)
            else:
                self.generateAccessToken()
                self.getInventorySummary(marketplace,nextToken)
        # print("Execution Completed")
        
    
    
def Values_Getter(region=Region.NA,marketplace=NA_Marketplace.US):
    # print("Value Getter Received")
    # print(region)
    # print(marketplace)
    caller = SPAPI_Caller(region)
    for data in caller.getInventorySummary(marketplace):
        values = list()
        print(data)
        for celldata in data:
            updated_date = str(datetime.datetime.now().date())
            asin = celldata.get("asin")
            sku = celldata.get("sellerSku")
            fnsku = celldata.get("fnSku")
            item_name = ""
            quantity = celldata.get("inventoryDetails").get("fulfillableQuantity")
            inbound_quantity = celldata.get("inventoryDetails").get("inboundReceivingQuantity")
            outbound_quantity = 0
            reviewing_quantity = 0
            damaged_quantity = celldata.get("inventoryDetails").get("unfulfillableQuantity").get("totalUnfulfillableQuantity")
            overall_quantity = int(celldata.get("inventoryDetails").get("fulfillableQuantity")) + int(celldata.get("inventoryDetails").get("unfulfillableQuantity").get("totalUnfulfillableQuantity"))
            warehouse = "FBA " + marketplace.value
            warehouse_id = ""
            unstructured_name = ""
            values.append((updated_date,
asin,
sku,
fnsku,
item_name,
quantity,
inbound_quantity,
outbound_quantity,
reviewing_quantity,
damaged_quantity,
overall_quantity,
warehouse,
warehouse_id,
unstructured_name))
        yield values