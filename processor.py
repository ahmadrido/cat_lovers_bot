import asyncpg
import json
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# Konfigurasi
API_KEY ="AIzaSyDptxjmiSlBpJfrnIiRbcKxOO-ZWJ3xz-I"
DB_PARAMS = "postgresql://array:123456@127.0.0.1:5435/catlovers_db"

# Model
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=API_KEY)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
google_api_key=API_KEY)

async def get_answer(user_query : str) -> str:
 
    # 1. Ubah pertanyaan user jadi vektor
    query_vector = await embeddings_model.aembed_query(user_query)
       
    query_vector_str = "[" + ",".join(map(str, query_vector)) + "]"
       
    # 2. Cari di Postgres yang paling mirip (Similarity Search)
    conn = await asyncpg.connect(DB_PARAMS)
    try:
        
        query = """
            SELECT content FROM cat_knowledge
            ORDER BY embedding <=> $1::vector 
            LIMIT 3;
        """
        results = await conn.fetch(query, query_vector_str)
        
        # Gabungkan hasil pencarian
        context = "\n".join([r['content'] for r in results]) if results else "Tidak ada informasi spesifik."
        
    finally:
        # Pastikan koneksi ditutup
        await conn.close()

    # 3. Kirim ke LLM untuk dijawab secara manusiawi
    prompt = f"""
        Kamu adalah asisten ahli kucing. 
    
        Konteks: {context}
        Pertanyaan: {user_query}
        """
   
    response = await llm.ainvoke(prompt)
    return str(response.content)