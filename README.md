# 🐱 CatLovers Bot

Bot Telegram berbasis AI untuk menjawab pertanyaan seputar kucing menggunakan RAG (Retrieval-Augmented Generation).

## ✨ Fitur

- 🤖 AI berbasis Google Gemini 2.5 Flash
- 🗄️ Database PostgreSQL dengan pgvector untuk similarity search
- 🔍 RAG (Retrieval-Augmented Generation) untuk jawaban yang akurat
- 💬 Bahasa Indonesia yang ramah dan informatif
- 📚 Knowledge base komprehensif tentang:
  - Nutrisi & Makanan
  - Kesehatan & Vaksinasi
  - Perilaku & Pelatihan
  - Panduan Perawatan
  - Jenis-jenis Kucing
  - Penyakit & Gejala

## 🚀 Teknologi

- **AI Model**: Google Gemini 2.5 Flash
- **Embeddings**: Google Generative AI (text-embedding-004)
- **Database**: PostgreSQL with pgvector extension
- **Bot Framework**: python-telegram-bot
- **Language**: Python 3.10+
- **Async**: asyncpg
- **LangChain**: langchain-google-genai

## 📋 Prerequisites

1. Docker & Docker Compose
2. Python 3.10 atau lebih tinggi
3. Google API Key untuk Gemini API 

## 🔧 Instalasi

### 1. Clone dan Setup Environment

```powershell
git clone https://github.com/ahmadrido/cat_lovers_bot.git
```

### 2. Setup Google API Key

Dapatkan Google API Key dari [Google AI Studio](https://makersuite.google.com/app/apikey) dan update di:
- [processor.py](processor.py): Ubah variabel `API_KEY`
- [ingest.py](ingest.py): Ubah variabel `API_KEY`

### 3. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

Dependencies yang dibutuhkan:
- `python-telegram-bot`: Framework untuk Telegram Bot
- `asyncpg`: Async PostgreSQL driver
- `psycopg2-binary`: PostgreSQL adapter untuk Python (untuk ingest.py)
- `langchain-google-genai`: Integration dengan Google AI (Gemini & Embeddings)

### 4. Start Docker Container PostgreSQL

```powershell
docker-compose up -d
```

Ini akan menjalankan PostgreSQL dengan pgvector extension (port 5435)

### 5. Setup Database Schema

```powershell
docker cp schema.sql catlovers_db:/schema.sql
docker exec -it catlovers_db psql -U array -d catlovers_db -f /schema.sql
```

### 6. Ingest Data ke Database

```powershell
python ingest.py
```

Proses ini akan:
- Membuat embeddings untuk seluruh knowledge base menggunakan Google AI
- Menyimpan data dan embeddings ke PostgreSQL
- Membutuhkan waktu beberapa menit tergantung koneksi internet

### 7. Update Bot Token

Edit [main.py](main.py) dan update `TOKEN` dengan Bot Token Telegram Anda.
Dapatkan token dari [@BotFather](https://t.me/botfather)

### 8. Jalankan Bot

```powershell
python main.py
```

## 📝 Perintah Bot

- `/start` - Mulai menggunakan bot
- `/help` - Tampilkan panduan penggunaan
- `/about` - Info tentang bot

## 🎯 Contoh Pertanyaan

- "Makanan apa yang berbahaya untuk kucing?"
- "Kapan kucing harus divaksin?"
- "Kenapa kucingku suka mencakar sofa?"
- "Bagaimana cara merawat bulu kucing?"
- "Apa gejala kucing sakit?"

## 🔒 Keamanan

Simpan token dan API key di environment variables atau gunakan file .env:

```powershell
# Set environment variables
$env:TELEGRAM_TOKEN = "your_telegram_bot_token"
$env:GOOGLE_API_KEY = "your_google_api_key"
$env:DB_PASSWORD = "your_database_password"
```

Atau buat file `.env` dan gunakan `python-dotenv` untuk load credentials.

## 🏗️ Arsitektur

```
User Question (Telegram)
     ↓
[Telegram Bot Handler]
     ↓
[Embedding Generation via Google AI]
     ↓
[Vector Similarity Search in PostgreSQL with pgvector]
     ↓
[Retrieve Top 3 Similar Documents]
     ↓
[Generate Answer via Gemini 2.5 Flash with RAG Context]
     ↓
[Clean Markdown Formatting]
     ↓
[Return to User via Telegram]
```

## 🆕 Fitur Utama

### RAG (Retrieval-Augmented Generation)

1. **Vector Similarity Search**: 
   - Menggunakan pgvector extension di PostgreSQL
   - Cosine similarity search untuk mencari dokumen relevan
   - Top-3 retrieval untuk konteks yang optimal

2. **Contextual Response Generation**:
   - System prompt yang terstruktur untuk personality bot
   - Fokus hanya pada topik kucing
   - Bahasa Indonesia yang ramah dan informatif
   - Automatic rejection untuk pertanyaan di luar topik

3. **Response Cleaning**:
   - Menghapus formatting markdown berlebihan
   - Output yang bersih dan mudah dibaca di Telegram

### Knowledge Base Komprehensif

- **Nutrisi & Makanan**: Makanan kering, basah, nutrisi penting, makanan berbahaya, porsi makan, snack
- **Kesehatan & Vaksinasi**: Jadwal vaksin, gejala penyakit, perawatan kesehatan
- **Perilaku & Pelatihan**: Litter box training, perilaku kucing, komunikasi kucing
- **Panduan Perawatan**: Grooming, perawatan bulu, kuku
- **Jenis-jenis Kucing**: Maine Coon, Persian, Siamese, dll
- **Penyakit & Gejala**: Feline Panleukopenia, masalah kesehatan umum

## 📊 Database Schema

### cat_knowledge (RAG Data)
- `id`: Primary key (SERIAL)
- `content`: Text content untuk knowledge base
- `category`: Kategori pengetahuan (Nutrisi, Kesehatan, Perilaku, dll)
- `embedding`: Vector embedding (pgvector, 768 dimensions untuk text-embedding-004)

Tabel ini menyimpan seluruh knowledge base yang akan di-retrieve saat user bertanya.

## 🐛 Troubleshooting

### Bot tidak merespon
- Pastikan Docker container PostgreSQL berjalan: `docker ps`
- Cek log database: `docker logs catlovers_db`
- Pastikan token Telegram valid
- Cek koneksi internet untuk akses Google AI API

### Error embedding atau LLM
- Pastikan Google API Key valid dan aktif
- Cek quota API di Google AI Studio
- Test API key dengan script sederhana
- Pastikan memiliki akses ke Gemini API

### Database connection error
- Cek PostgreSQL container: `docker logs catlovers_db`
- Verify credentials di [processor.py](processor.py) dan [ingest.py](ingest.py)
- Pastikan port 5435 tidak digunakan aplikasi lain
- Test koneksi: `docker exec -it catlovers_db psql -U array -d catlovers_db`

### Error saat ingest data
- Pastikan schema.sql sudah dijalankan
- Cek apakah pgvector extension terinstall
- Pastikan koneksi ke Google AI API stabil
- Proses ingest membutuhkan waktu, tunggu hingga selesai

## 🗂️ Struktur File

```
chatbot-catlovers/
├── main.py              # Entry point bot Telegram
├── processor.py         # RAG logic & Gemini integration
├── ingest.py           # Data ingestion & embeddings
├── docker-compose.yml  # Docker configuration
├── schema.sql          # Database schema
├── data.py            # Data helper (jika ada)
├── test_db.py         # Database testing
├── tes_api.py         # API testing
└── README.md          # Documentation
```

## 📄 License

Educational Project - 2025

## 👨‍💻 Author

Created by Array Team (kelompok 5)
Nur Rizqi Tegar Wibawa
Ahmad Rido Kamaludin
Haidir Arraysach Saputra

## 🙏 Acknowledgments

- Google AI untuk Gemini API dan Embeddings
- Ankane untuk pgvector PostgreSQL extension
- Python Telegram Bot library
- LangChain untuk Google AI integration
