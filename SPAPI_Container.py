from enum import Enum
from typing import Union
from pathlib import Path
import os
import dotenv


dotenv.load_dotenv(Path(__file__).resolve().parent / ".env")

class Region(str,Enum):
    NA = "na"
    EU = "eu"
    FE = "fe"
    
    
class NA_Marketplace(str,Enum):
    US = "US"
    CA = "CA"
    MX = "MX"
    BR = "BR"
    
class EU_Marketplace(str,Enum):
    UK = "UK"
    DE = "DE"
    FR = "FR"
    IT = "IT"
    ES = "ES"
    NL = "NL"
    SE = "SE"
    PL = "PL"
    BE = "BE"
    TR = "TR"
    AE = "AE"
    SA = "SA"
    
class FE_Marketplace(str,Enum):
    JP = "JP"
    AU = "AU"
    SG = "SG"
    IN = "IN"

class SPAPI_Container:
    Region = Region
    NA_Marketplace = NA_Marketplace
    EU_Marketplace = EU_Marketplace
    FE_Marketplace = FE_Marketplace
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    app_id = os.getenv("app_id")
    refresh_token_map = {
        "na":os.getenv("na_refresh_token"),
        "eu":os.getenv("eu_refresh_token"),
        "fe":os.getenv("fe_refresh_token")
    }
    marketplace_id_map = {
    "region": {
            "na": {
                "US": "ATVPDKIKX0DER",
                "CA": "A2EUQ1WTGCTBG2",
                "MX": "A1AM78C64UM0Y8",
                "BR": "A2Q3Y263D00KWC"
            },
            "eu": {
                "UK": "A1F83G8C2ARO7P",
                "DE": "A1PA6795UKMFR9",
                "FR": "A13V1IB3VIYZZH",
                "IT": "APJ6JRA9NG5V4",
                "ES": "A1RKKUPIHCS9HS",
                "NL": "A1805IZSGTT6HS",
                "SE": "A2NODRKZP88ZB9",
                "PL": "A1C3SOZRARQ6R3",
                "BE": "AMEN7PMS3EDWL",
                "TR": "A33AVAJ2PDY3EV",
                "AE": "A2VIGQ35RCS4UG",
                "SA": "A17E79C6D8DWNP"
            },
            "fe": {
                "JP": "A1VC38T7YXB528",
                "AU": "A39IBJ37TRP1C6",
                "SG": "A19VAU5U5O7RUS",
                "IN": "A21TJRUUN4KGV"
                }
        }
    }