from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import pandas as pd 
import os
from dotenv import load_dotenv

load_dotenv()

class MongoService:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('MONGODB_DB')]
        self.collection = self.db[os.getenv('MONGODB_COLLECTION')]
        self.create_indexes()
    def insert_dataframe(self,df:pd.DataFrame):
        records = df.to_dict(orient='records')
        if not records:
            print('No record to insert')
            return
        try:
            self.collection.insert_many(records, ordered=False)
            print(f'Inserted {len(records)} records into MongoDB')
        except BulkWriteError as e:
            print('Some duplicate records were skipped')
    
    def create_indexes(self):
        ''''
        create indexe for faster queries
        '''
        self.collection.create_index(
            [("brand",1),("model",1)],
            unique = True
        )
        self.collection.create_index('price_segment')
        self.collection.create_index('gaming_score')

        print('MongoDB indexes created')
    
    def count_documents(self):
        return self.collection.count_documents({})
    

