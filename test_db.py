import psycopg2
import sys

try:
    # docker-compose
    conn = psycopg2.connect("postgresql://array:123456@127.0.0.1:5435/catlovers_db")
    print("✅ Koneksi ke Docker Postgres BERHASIL!")
    
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print(f"PostgreSQL version: {db_version}")
    
    cur.close()
    conn.close()
except psycopg2.Error as e:
    print("❌ KONEKSI GAGAL!")
    print(f"Error: {e}")
    sys.exit(1)