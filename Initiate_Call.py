from .sp_api_caller import SP_API_Caller,Region,NA_Marketplace,EU_Marketplace,FE_Marketplace

caller = SP_API_Caller()
caller.setRegionMarketplace(region=Region.NA,marketplace=NA_Marketplace.US)
caller.generateAccessToken()
caller.GetInventorySummary()