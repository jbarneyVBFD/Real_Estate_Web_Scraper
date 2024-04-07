import pandas as pd

df = pd.read_csv('Temp/addresses_commercial.csv')

print(df)

df.index = range(len(df))

df = df.drop(columns=['Unnamed: 0'])

df = df[df['Grantors'] != '[]']

df.index = range(len(df))

print(df)

df.to_csv('addresses_commercial_final.csv')