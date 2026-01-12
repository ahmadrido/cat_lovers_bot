from langchain_google_genai import GoogleGenerativeAIEmbeddings

API_KEY = "AIzaSyBrYaHxfT0QOIgqVwUfeheOxgHE3xYyvZQ"

try:
    print("Sedang mencoba menghubungi Google AI...")
    embeddings = GoogleGenerativeAIEmbeddings(model="text-embedding-004", google_api_key=API_KEY)
    vector = embeddings.embed_query("Halo kucing lucu")
    print("✅ MANTAP! API Key berfungsi, vektor berhasil dibuat.")
except Exception as e:
    
    print(f"❌ WADUH! Masih error: {e}")