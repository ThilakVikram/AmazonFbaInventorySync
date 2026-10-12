import requests
import time
from .SPAPI_Container import SPAPI_Container,Region,NA_Marketplace,EU_Marketplace,FE_Marketplace
from typing import Union
class SP_API_Caller(SPAPI_Container):
    marketplaceID = None
    region = None
    marketplace = None
    access_token = None
    def __init__(self):
        pass
    def setRegionMarketplace(self,region:Region,marketplace:Union[NA_Marketplace,EU_Marketplace,FE_Marketplace]):
        # print(self.marketplace_id_map)
        self.marketplaceID = self.marketplace_id_map.get("region").get(region.value).get(marketplace.value)
        self.region = region.value
        self.marketplace = marketplace.value
        pass
    def generateAccessToken(self):
        if None in {self.region,self.marketplace,self.marketplaceID}:
            raise Exception("Set Region and Marketplace Using setRegionMarketplace before using generate or get function")
        url = f"https://api.amazon.com/auth/o2/token?grant_type=refresh_token&refresh_token={self.refresh_token_map.get(self.region)}&client_id={self.client_id}&client_secret={self.client_secret}"
        headers = {
            "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8"
        }
        response = requests.post(
            url,
            headers=headers)
        response.raise_for_status()
        response.json().get("access_token")
        pass
    def AuthHeader(self,access_token):
        return {
            "x-amz-access-token":access_token
        }
        pass
    def StatusError(self,code):
        match code:
            case 400:
                raise Exception("Missing or Invalid Parameter")
            case 404:
                raise Exception("Resource Not Exist")
            case 500:
                raise Exception("Unexpected Error")
            case 503:
                raise Exception("Server Error")
        pass
    def GetInventorySummary(self):
        url = f"https://sellingpartnerapi-na.amazon.com/fba/inventory/v1/summaries?details=false&granularityType=Marketplace&granularityId={self.marketplaceID}&marketplaceIds={self.marketplaceID}"
        headers = self.AuthHeader(self.access_token)
        response = requests.get(url,headers=headers)
        match response.status_code:
            case 200:
                return response.json()
            case 429:
                time.sleep(3)
                self.GetInventorySummary()
            case 403:
                self.generateAccessToken()
                self.GetInventorySummary()
            case _:
                self.StatusError(response.status_code)
                pass
    
