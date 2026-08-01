import pandas as pd
from datetime import datetime
def transform_data(data):
    rows=[]
    for coin,value in data.items():
        rows.append({
            "coin_name":coin,
            "price":value['usd'],
            "time_stamp":datetime.now()
            })
    df=pd.DataFrame(rows)
    print("transform completed")
    return df