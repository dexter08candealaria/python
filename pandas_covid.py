import numpy as np
import pandas as pd
import os
import urllib
%matplotlib inline

url = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
file_path = os.path.join("data","covid")

os.makedirs(file_path, exist_ok=True)
csv_path = os.path.join(file_path,"WHO-COVID-19-global-data.csv")
urllib.request.urlretrieve(url,csv_path)
df = pd.read_csv(csv_path)
df
df_index = df.index
df_index
df_cols = df.columns
df_cols
df_index.values
df.values
df.dtypes
df.shape
df.head()
df.head()
df.info()
df.describe()
df['Country']
df['Country'].unique()
df.columns = [col.strip() for col in df.columns]
df.columns
df.Country
df.loc[1:4,'Country']
df.loc[1:8,['Country','New_cases']]
df.Country == 'Philippines'
df[df.Country == 'Philippines']
df.loc[df.New_deaths > 1000, ['New_deaths','Country']]
df.loc[(df.New_deaths > 10) & (df.Country == 'Philippines')],['Date_reported', 'Country_code', 'Country', 'WHO_region', 'New_cases',
       'Cumulative_cases', 'New_deaths', 'Cumulative_deaths']
df['pct_cases'] = (df['New_cases']) / (df['Cumulative_cases']) * 100
df
df.loc[df.Country == 'Philippines']

