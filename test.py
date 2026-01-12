import google.generativeai as genai
import os

# 1. Masukkan API Key kamu di sini
API_KEY = "AIzaSyBrYaHxfT0QOIgqVwUfeheOxgHE3xYyvZQ"

try:
    genai.configure(api_key=API_KEY)
    
    # 2. Inisialisasi Model
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # 3. Kirim Chat Sederhana
    print("Sedang mencoba menghubungi Gemini...")
    response = model.generate_content("Halo Gemini, apakah kamu aktif? Jawab singkat saja.")
    
    print("-" * 30)
    print("Respon Gemini:", response.text)
    print("-" * 30)
    print("✅ Koneksi Berhasil!")

except Exception as e:
    print("-" * 30)
    print("❌ Terjadi Error:")
    print(e)
    print("-" * 30)