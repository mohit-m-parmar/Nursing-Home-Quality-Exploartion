import io
import csv
import math
import psycopg2
import numpy as np
import pandas as pd
import json as simplejson
from pymongo import MongoClient
from sqlalchemy import create_engine
#import database


		
engine = create_engine('postgresql+psycopg2://nursing_home:nursing_home@localhost:5432/nursing_home')

# This will insert data in postgresql database
facility_df= pd.read_csv('facility.csv')
facility_df.to_sql('facility', engine, if_exists='append', index=False)



measurment_df= pd.read_csv('measurment.csv')
measurment_df.to_sql('measurment', engine, if_exists='append', index=False)

nursing_home_quality_df = pd.read_csv('nursing_home_quality.csv')
nursing_home_quality_df.to_sql('nursing_home_quality', engine, if_exists='append', index=False)


# #This will load JSON Data to mongoDB 
# mongo_client=MongoClient("mongodb://localhost:27017/") 
# myDb=mongo_client['BedCensus']
# information=myDb.nursinghomebedcensus

# with open('convertjson.json') as f:
#     file_data = simplejson.load(f)

# information.insert_one(file_data)


print('data loaded successfully')
						