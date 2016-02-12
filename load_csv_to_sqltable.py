# requires pip install numpy and pip install pandas

import pandas as pd
df = pd.read_csv('BUILD-sites.csv')
df.columns = [c.lower() for c in df.columns] #postgres doesn't like capitals or spaces

print df

from sqlalchemy import create_engine
engine = create_engine('postgresql:///build_reads') # postgresql:///<yourdbhere>

df.to_sql("sites", engine) # (<yourdbhere>, engine)