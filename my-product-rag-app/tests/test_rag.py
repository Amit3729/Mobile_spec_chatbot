from app.services.rag_service import RAGService

def main():
    rag = RAGService()

    quarry = "Best gamming phone under 50000NPR"
    answer = rag.answer(quarry)
    print('\nQUESTION:')
    print(quarry)

    print('/nANSWER')
    print(answer)

if __name__ == '__main__':
    main()