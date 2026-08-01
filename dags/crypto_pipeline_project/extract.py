import requests as req
import json
import time
def extract_data():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,bnb,xrp,usdc,solana,tron&vs_currencies=usd"
    all_coins=["bitcoin","ethereum","tether","bnb","xrp","usdc","solana","tron"]
    
    def fetch_data(coins):
        params={
            "ids": ",".join(coins),
            "vs_currencies": "usd"
        }
        response=req.get(url,params=params)
        
        if response.status_code==200:
            return response.json()
        return {}
    data=fetch_data(all_coins)
    
    for attempts in range(3):
        missing=[coin for coin in all_coins if coin not in data]
        if not missing:
            break
        print(f"this data :{missing} is missing , retrying...({attempts+2})")
        time.sleep(2)
        retried=fetch_data(missing)
        data.update(retried)
    still_missing=[coin for coin in all_coins if coin not in data]
    if still_missing:
        print(f"Still missing data for: {still_missing}")
    for coin in all_coins:
        if coin in data:
            print(f"{coin:10} ${data[coin]['usd']:,.4f}")
    print("extract completed")
    return data