import os
import asyncpg
import json
import re
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# Konfigurasi
API_KEY = os.getenv("GOOGLE_API_KEY")
DB_PARAMS = "postgresql://array:123456@127.0.0.1:5435/catlovers_db"

def clean_markdown(text: str) -> str:
    """Membersihkan markdown formatting dari text"""
    # Hapus bold (**text** atau __text__)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    
    # Hapus italic (*text* atau _text_)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    
    # Ubah bullet points markdown menjadi dash sederhana
    text = re.sub(r'^\*\s+', '- ', text, flags=re.MULTILINE)
    
    return text.strip()

# Model
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=API_KEY)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
google_api_key=API_KEY)

async def get_answer(user_query : str) -> str:
 
    # 1. Ubah pertanyaan user jadi vektor
    query_vector = await embeddings_model.aembed_query(user_query)
       
    query_vector_str = "[" + ",".join(map(str, query_vector)) + "]"

    # System Prompt
    SYSTEM_PROMPT = """ Kamu adalah chatbot virtual bernama "CatLovers Bot".
    Peran kamu:
    - Ahli dasar tentang kucing (makanan, kesehatan umum, perilaku, perawatan).
    - Membantu pemilik kucing dengan bahasa yang ramah dan mudah dipahami.

    Gaya bicara:
    - Gunakan Bahasa Indonesia yang santai, sopan, dan hangat.
    - Jangan terlalu panjang, tapi tetap informatif.
    - Gunakan poin atau daftar jika perlu agar mudah dibaca.
    - Hindari istilah medis yang rumit kecuali diminta.

    Aturan jawaban:
    - Fokus pada kucing, jangan melebar ke hewan lain.
    - Jika pertanyaan berpotensi berbahaya (kesehatan serius), sarankan konsultasi ke dokter hewan.
    - Jangan mengarang fakta yang tidak pasti.
    - Jika tidak tahu, jujur dan beri saran aman.

    Aturan MUTLAK:
    - Kamu HANYA boleh menjawab pertanyaan tentang kucing.
    - Jika pertanyaan TIDAK berhubungan dengan kucing, kamu HARUS menolak dengan sopan.
    - Jangan pernah menjawab pertanyaan tentang manusia, hewan lain, atau topik umum.
    - Jangan mengarang jawaban di luar konteks kucing.

    Akhiri jawaban dengan satu kalimat ramah (opsional), misalnya:
    "Semoga membantu ya! 🐾"
    """
       
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
        prompt = f"""{SYSTEM_PROMPT}
        Konteks informasi yang relevan:
        {context}

        Pertanyaan pengguna: {user_query}
        """
   
    response = await llm.ainvoke(prompt)
    
    # Bersihkan markdown formatting dari response
    clean_response = clean_markdown(str(response.content))
    
    return clean_response