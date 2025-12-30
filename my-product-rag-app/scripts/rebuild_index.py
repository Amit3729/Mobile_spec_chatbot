from app.services.mongo_service import MongoService
from app.services.embedding import EmbeddingService

def main():
    print('Vector indec rebuild....')
    #load data from mongodb
    mongo = MongoService()
    documents = list(mongo.collection.find({}, {'_id': 0}))

    if not documents:
        print('No documents are found in MongoDB')
        return
    print(f'Loaded {len(documents)} documents from MongoDB')

    #Initilize embedding service
    embedder = EmbeddingService()

    #Index documents into Qdrant
    embedder.index_documents(documents)

    print("Vector indexing completed Successfully")

if __name__ == "__main__":
    main()
    