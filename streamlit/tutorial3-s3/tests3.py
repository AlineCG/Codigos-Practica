import pandas as pd
import boto3
client = boto3.client('s3')
path='s3://testbucket-lanek-0/carpeta0/footbal_data1.csv'
df=pd.read_csv(path)
#df.head()
print('juju')
print(df.to_string())
print('holiwis')
