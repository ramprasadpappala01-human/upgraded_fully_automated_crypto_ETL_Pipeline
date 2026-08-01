from sqlalchemy import create_engine
import pandas as pd
def load_data(df):
    
    #creating enginer to load data into postgresql using coin_dim and date_dim to get required ids for fact table
    engine=create_engine("postgresql://airflow:airflow@postgres:5432/rtcpp")
    coin_dim=pd.read_sql("SELECT coin_id , coin_name FROM coin_dim",engine)
    date_dim=pd.read_sql("SELECT full_date , date_id FROM date_dim",engine)
    date_dim["full_date"] = pd.to_datetime(date_dim["full_date"]).dt.date 
    
    #finding new coins by comparing with coin_dim and loading them into coin_dim
    new_coins=set(df['coin_name'])-set(coin_dim['coin_name'])
    if new_coins:
        new_coins_df=pd.DataFrame({"coin_name":list(new_coins)})
        new_coins_df.to_sql("coin_dim",engine,if_exists='append',index=False)
        coin_dim=pd.read_sql("SELECT coin_id,coin_name FROM coin_dim",engine)
    
    #merging coin_dim with our data to get coin_id for fact table   
    df=df.merge(coin_dim,on='coin_name',how="left")
    
    #converting time_stamp to correct format 
    df['full_date']=df['time_stamp'].dt.date
    date_dim["full_date"]=pd.to_datetime(date_dim["full_date"]).dt.date
    
    #finding new dates by comparing with date_dim and loading them into date_dim
    new_dates=set(df['full_date'])-set(date_dim['full_date'])
    if new_dates:
        new_df=pd.DataFrame({"full_date":list(new_dates)})
        new_df['full_date']=pd.to_datetime(new_df['full_date'])
        new_df['year']=new_df['full_date'].dt.year
        new_df['month']=new_df['full_date'].dt.month
        new_df['day']=new_df['full_date'].dt.day
        new_df.to_sql("date_dim",engine, if_exists='append',index=False)
        date_dim=pd.read_sql("SELECT full_date,date_id FROM date_dim",engine)
        
    #merging date_dim with our data to get date_id for fact table
    df=df.merge(date_dim,on="full_date",how='left')
    
    #selecting required columns for fact table and loading into fact table
    fact_df=df[['coin_id','date_id','price','time_stamp']].rename(columns={"time_stamp":"last_updated"})
    fact_df.to_sql('fact_crypto_prices',engine, if_exists='append',index=False)
    print(fact_df)
    print("load completed")
