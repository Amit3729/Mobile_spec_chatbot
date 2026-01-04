import redis
import os

from dotenv import load_dotenv

load_dotenv()

class CacheService:
    def __init__(self):
        self.client = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            decode_responses=True
        )
    def check(self,prompt):
        return self.get(prompt)
    
    def store(self, prompt:str, response:str, ttl:int=3600):
        self.set(prompt,response,ttl)

    def get(self,key:str):
        return self.client.get(key)
    
    def set(self, key:str, value:str, ttl:int = 3600):
        self.client.setex(key, ttl, value)
        