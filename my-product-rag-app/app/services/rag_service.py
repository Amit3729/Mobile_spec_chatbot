import os
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class RAGService:
    def __init__(self,
                 collection_name:str = 'mobile-spec',
                 embedding_model:str = 'all-MiniLM-L6-v2',
                 top_k: int = 5):
        self.collection_name = collection_name
        self.top_k = top_k

        #Embedding model
        self.embbeder = SentenceTransformer(embedding_model)
        #Qudrant cloud client
        self.qdrant = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        #LLM Client
        self.llm = Groq(api_key=os.getenv("GROQ_API_KEY"))

    #Retrive revelent documents from Qdrant
    def retrive(self, query):
        query_vector = self.embbeder.encode(query).tolist()

        search_result = self.qdrant.search(
            collection_name =self.collection_name,
            query_vector = query_vector,
            limit=self.top_k
        )
        documents = [hit.playload for hit in search_result]
        return documents
    #Build Promt for LLM
    def build_promt(self,query:str,documents: list)->str:
        context = "n\n".join(
            f"-{doc['description_text']}" for doc in documents

        )
        
        prompt = f'''
You are a smartphone expert assistant.
Use the Information below to answer the user's question.
if the answer is not present, say you don't know in polite manner.

Context:
{context}

Questio:
{query}

Answer:

'''
        return prompt
    
    #Generate final Answer
    def answer(self, query):
        documents = self.retrive(query)

        if not documents:
            return "Sorry, I couldn't find revelent information."
        
        prompt = self.build_promt(query,documents)

        response = self.llm.chat.completions.create(
            model='llama-3.1-8b-instant',
            messages=[{'role':'user','content':prompt}],
            temperature=0.3


        )

        return response.choices[0].message.content