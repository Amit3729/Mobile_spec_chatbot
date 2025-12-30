from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid
import os
class EmbeddingService:
    def __init__(self,
                 collection_name: str = 'mobile-specs',
                 model_name: str = 'all-MiniLM-L6-v2'
                 ):
        self.collection_name = collection_name
        self.client = QdrantClient(url=os.getenv('QDRANT_URL'),
                                    api_key=os.getenv('QDRANT_API_KEY'))
        self.model = SentenceTransformer(model_name)

        self._ensure_collection()
    
    def _ensure_collection(self):
        vector_size = self.model.get_sentence_embedding_dimension()
        collections = [c.name for c in self.client.get_collections().collections]

        if self.collection_name not in collections:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size,
                                            distance=Distance.COSINE)
            )
            print("Qdrant collection created")
        else:
            print("Qdrant collection already exists")

    def index_documents(self, documents:list):
        points = []

        for doc in documents:
            text = doc.get('description_text')
            if not text:
                continue

            vector = self.model.encode(text).tolist()
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload=doc
                )
            )
        if not points:
            print("No vectors to insert")
            return
        
        self.client.upsert(
            collection_name= self.collection_name,
            points=points
        )
        print(f'Indexed {len(points)} documents into Qdrant')
        

        
        