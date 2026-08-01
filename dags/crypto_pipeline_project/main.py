from extract import extract_data
from transform import transform_data
from load import load_data
data=extract_data()
df=transform_data(data)
load_data(df)

print("pipeline completed succesfully")