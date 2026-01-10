
import psycopg2
from psycopg2.extras import execute_values
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# 1. Konfigurasi
API_KEY = "AIzaSyDptxjmiSlBpJfrnIiRbcKxOO-ZWJ3xz-I"
DB_PARAMS = "postgresql://array:123456@127.0.0.1:5435/catlovers_db"

embeddings_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=API_KEY)

knowledge_data = [
    {"cat": "Nutrisi & Makanan","text": "Makanan basah memiliki kelebihan: kandungan air tinggi (75-80%) yang membantu hidrasi kucing, lebih mudah dicerna, aroma lebih menarik untuk kucing, dan cocok untuk kucing dengan masalah ginjal. Kekurangannya: lebih mahal, cepat basi jika tidak dihabiskan, harus disimpan di kulkas setelah dibuka, dan tidak membantu membersihkan gigi. Ideal dikombinasikan dengan makanan kering untuk nutrisi seimbang."},
    {"cat": "Nutrisi & Makanan","text": "Makanan kering untuk kucing memiliki beberapa kelebihan: lebih ekonomis dan tahan lama, membantu membersihkan gigi kucing, mudah disimpan tanpa pendingin, dan praktis untuk pemberian makan otomatis. Namun ada kekurangannya: kandungan air rendah (8-10%), dapat menyebabkan dehidrasi jika kucing kurang minum. Rekomendasi: berikan 2-3 kali sehari sesuai berat badan, pastikan air minum selalu tersedia."},
    {"cat": "Nutrisi & Makanan","text": "Makanan basah memiliki kelebihan: kandungan air tinggi (75-80%) yang membantu hidrasi kucing, lebih mudah dicerna, aroma lebih menarik untuk kucing, dan cocok untuk kucing dengan masalah ginjal. Kekurangannya: lebih mahal, cepat basi jika tidak dihabiskan, harus disimpan di kulkas setelah dibuka, dan tidak membantu membersihkan gigi. Ideal dikombinasikan dengan makanan kering untuk nutrisi seimbang."},
    {"cat": "Nutrisi & Makanan","text": "Nutrisi penting untuk kucing: Protein minimal (26%) untuk kucing dewasa dan (30%) untuk anak kucing. Taurin adalah asam amino esensial untuk kesehatan jantung dan mata. Lemak minimal (9%) untuk energi dan kesehatan bulu. Air: kucing perlu 60ml air per kg berat badan per hari. Vitamin dan mineral seperti Vitamin A, D, E, kalsium, dan fosfor penting untuk tulang dan sistem imun."},
    {"cat": "Nutrisi & Makanan","text": "Makanan berbahaya untuk kucing yang harus dihindari: Cokelat mengandung theobromine yang beracun. Bawang merah dan bawang putih merusak sel darah merah. Susu sapi karena banyak kucing dewasa lactose intolerant. Anggur dan kismis dapat menyebabkan gagal ginjal. Kafein beracun untuk kucing. Tulang ayam dapat menyebabkan tersedak atau luka dalam."},
    {"cat": "Kesehatan & Vaksinasi","text": "Vaksinasi Tricat/F3 melindungi dari Feline Panleukopenia, Calicivirus, dan Rhinotracheitis. Jadwal: usia 8-9 minggu (pertama), 12 minggu (kedua), kemudian booster tahunan. Vaksinasi ini melindungi dari virus mematikan yang menyerang sistem pencernaan dan pernapasan kucing."},
    {"cat": "Kesehatan & Vaksinasi","text": "Vaksinasi Rabies diberikan pada usia 16 minggu dengan booster tahunan. Vaksinasi ini melindungi dari virus rabies yang mematikan dan dapat menular ke manusia. Vaksinasi rabies sangat penting terutama jika kucing sering keluar rumah atau berinteraksi dengan hewan lain."},
    {"cat": "Kesehatan & Vaksinasi","text": "Vaksinasi opsional untuk kucing: Chlamydia untuk kucing yang sering berinteraksi dengan kucing lain. Feline Leukemia Virus (FeLV) untuk kucing yang keluar rumah atau tinggal di multi-cat household. Konsultasikan dengan dokter hewan untuk menentukan vaksinasi yang diperlukan."},
    {"cat": "Kesehatan & Vaksinasi","text": "Tanda-tanda kucing sehat: mata jernih dan cerah, hidung lembab dan bersih, bulu mengkilap dan tidak rontok berlebihan, nafsu makan baik, aktif dan responsif, berat badan stabil, dan buang air normal. Perhatikan perubahan pada tanda-tanda ini untuk deteksi dini masalah kesehatan."},
    {"cat": "Perilaku & Pelatihan", "text": "Perawatan litter box: Buang kotoran minimal 2x sehari. Ganti semua pasir dan cuci kotak setiap minggu. Kucing sangat bersih, jika kotak kotor mereka akan pipis sembarangan. Jangan letakkan dekat mesin cuci, area ramai, atau sudut sempit yang menakutkan."},
    {"cat": "Perilaku & Pelatihan", "text": "Mengatasi kucing pipis sembarangan: Periksa kebersihan litter box, cek apakah ada masalah kesehatan seperti ISK, evaluasi perubahan di rumah yang bisa menyebabkan stress, tambah jumlah litter box, dan bersihkan area yang dikotori dengan enzymatic cleaner. Jangan hukum kucing karena ini kontraproduktif."},
    {"cat": "Perilaku & Pelatihan","text": "Alasan kucing mencakar: mengasah dan merawat kuku, menandai teritorial karena ada kelenjar di telapak kaki, peregangan otot, dan melepas stress serta energi. Ini adalah perilaku alami yang tidak bisa dihilangkan, hanya dialihkan ke tempat yang tepat."},
    {"cat": "Perilaku & Pelatihan","text": "Solusi mencakar furnitur: Sediakan scratching post yang kokoh dan tinggi (minimal 75cm), letakkan di area favorit kucing, gunakan bahan sisal, kardus, atau karpet. Sediakan beberapa di lokasi berbeda. Latih dengan meletakkan catnip di scratching post, beri pujian dan reward saat menggunakannya. Potong kuku setiap 2-3 minggu. Jangan pernah declawing karena merupakan amputasi yang menyakitkan."},
    {"cat": "Perilaku & Pelatihan","text": "Bahasa tubuh kucing - Ekor: Ekor tegak berarti senang, ramah, siap berinteraksi. Ekor mengibas cepat berarti kesal, frustrasi, jangan ganggu. Ekor di antara kaki berarti takut atau cemas. Ekor membesar seperti sikat botol berarti sangat ketakutan atau agresif."},
    {"cat": "Perilaku & Pelatihan","text": "Bahasa tubuh kucing - Telinga dan mata: Telinga tegak maju berarti penasaran dan waspada. Telinga ke belakang berarti marah, defensif, siap menyerang. Pupil melebar bisa berarti takut, excited, atau mode berburu."},
    {"cat": "Perilaku & Pelatihan","text": "Sosialisasi anak kucing: Periode kritis adalah usia 2-7 minggu. Perkenalkan berbagai orang, suara, dan pengalaman positif. Lakukan handling lembut setiap hari. Bermain dengan mainan interaktif. Sosialisasi yang baik di periode ini akan menghasilkan kucing dewasa yang percaya diri dan ramah."},
    {"cat": "Panduan Perawatan","text": "Menyisir bulu kucing: Untuk bulu pendek 1-2x seminggu, bulu panjang setiap hari. Gunakan sisir gigi lebar, slicker brush, atau sisir kutu. Mulai dari kepala ke ekor, berhati-hati di area sensitif. Manfaatnya: mengurangi hairball, mencegah bulu kusut, deteksi dini masalah kulit, dan bonding time dengan kucing."},
    {"cat": "Panduan Perawatan","text": "Memandikan kucing: Frekuensi setiap 4-6 minggu atau saat sangat kotor. Kucing membersihkan diri sendiri sehingga tidak perlu terlalu sering. Gunakan air hangat dan shampo khusus kucing (pH balanced). Hindari area mata, telinga, dan hidung. Bilas hingga bersih dan keringkan dengan handuk atau hair dryer suhu rendah. Mulai saat masih kecil agar terbiasa."},
    {"cat": "Panduan Perawatan","text": "Memotong kuku kucing: Lakukan setiap 2-3 minggu menggunakan gunting kuku khusus kucing. Tekan telapak lembut agar kuku keluar, potong hanya bagian putih/transparan, hindari quick (bagian pink berisi pembuluh darah). Jika berdarah gunakan styptic powder. Lakukan saat kucing rileks atau mengantuk, beri reward setelahnya."},
    {"cat": "Panduan Perawatan","text": "Kebersihan telinga kucing: Periksa setiap minggu, bersihkan jika perlu (setiap 2-4 minggu). Gunakan ear cleaner khusus kucing atau NaCl 0.9%. Teteskan ke lubang telinga, pijat pangkal telinga, biarkan kucing menggelengkan kepala, lap bagian luar dengan kapas. JANGAN masukkan cotton bud ke dalam telinga. Ke dokter jika ada kotoran berlebihan, bau tidak sedap, atau kucing sering menggaruk telinga."},
    {"cat": "Panduan Perawatan","text": "Kebersihan gigi kucing: Penting untuk mencegah karang gigi, gingivitis, dan penyakit periodontal. Sikat gigi ideal 2-3x seminggu menggunakan sikat gigi jari atau sikat kecil dengan pasta gigi khusus kucing (jangan pasta gigi manusia). Alternatif: dental treats, mainan dental, makanan kering, atau air additive. Scaling di dokter hewan setiap 1-2 tahun jika diperlukan."},
    {"cat": "Panduan Perawatan","text": "Kebersihan mata kucing: Lap kotoran mata dengan kapas basah air hangat, bersihkan dari sudut dalam ke luar. Gunakan kapas berbeda untuk setiap mata. Sedikit kotoran di sudut mata saat bangun tidur adalah normal. Tidak normal jika ada kotoran berlebihan berwarna kuning/hijau, mata merah dan berair terus, mata tertutup atau bengkak, atau selaput putih menutup mata."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Kucing selalu jatuh dengan empat kaki dan tidak pernah terluka. FAKTA: Kucing memiliki righting reflex, tapi tetap bisa terluka parah atau mati dari ketinggian. Jatuh dari lantai 2-7 paling berbahaya karena kucing tidak punya cukup waktu untuk posisi landing yang benar."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Kucing tidak butuh perhatian dan mandiri total. FAKTA: Kucing butuh stimulasi mental, interaksi sosial, dan perhatian. Mereka bisa kesepian dan stress jika diabaikan. Kucing adalah hewan sosial yang membentuk ikatan dengan pemiliknya."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Kucing yang dimandulkan akan jadi gemuk dan malas. FAKTA: Penambahan berat badan terjadi karena metabolisme berubah setelah sterilisasi, tapi bisa dikontrol dengan diet yang tepat dan olahraga. Manfaat sterilisasi jauh lebih besar daripada risiko obesitas yang bisa dicegah."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Kucing hitam membawa sial. FAKTA: Takhayul tanpa dasar ilmiah. Di beberapa budaya seperti Jepang dan Inggris, kucing hitam justru dianggap pembawa keberuntungan. Warna bulu tidak mempengaruhi kepribadian atau membawa nasib."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Kucing bisa melihat hantu atau makhluk gaib. FAKTA: Kucing memiliki pendengaran dan penglihatan superior yang mendeteksi gerakan kecil dan suara ultrasonic yang manusia tidak bisa dengar atau lihat. Mereka bisa mendengar frekuensi hingga 64 kHz (manusia hanya 20 kHz)."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Kucing punya 9 nyawa. FAKTA: Hanya metafora untuk ketahanan dan kelincahan kucing. Mereka tetap makhluk hidup dengan satu nyawa. Ungkapan ini muncul karena kemampuan kucing bertahan dari situasi berbahaya dan refleks yang luar biasa."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Mendengkur selalu berarti kucing senang. FAKTA: Kucing juga mendengkur saat sakit, stress, atau kesakitan sebagai mekanisme self-soothing atau self-healing. Perhatikan konteks dan tanda-tanda lain untuk memahami kondisi kucing."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Kucing dan anjing selalu musuhan. FAKTA: Dengan sosialisasi yang tepat sejak kecil, kucing dan anjing bisa hidup harmonis bahkan berteman baik. Banyak rumah tangga sukses memelihara kedua hewan ini bersama-sama."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Whisker (kumis) kucing boleh dipotong. FAKTA: JANGAN PERNAH memotong whisker! Whisker adalah sensor penting untuk navigasi, keseimbangan, dan orientasi ruang. Memotongnya membuat kucing disorientasi dan kesulitan bergerak di ruang gelap."},
    {"cat": "Perilaku & Pelatihan","text": "Mendengkur pada kucing bisa memiliki arti berbeda tergantung konteks. Kucing mendengkur saat merasa senang dan nyaman, tetapi juga bisa mendengkur saat sakit atau stress sebagai mekanisme self-soothing. Beberapa penelitian menunjukkan frekuensi dengkuran (25-150 Hz) dapat membantu penyembuhan tulang dan mengurangi rasa sakit."},
    {"cat": "Perilaku & Pelatihan","text": "Menggigit pada kucing memiliki arti berbeda. Gigitan halus biasanya adalah bentuk main-main atau kasih sayang (love bite). Gigitan keras berarti kucing sudah mencapai batas kesabaran dan meminta untuk berhenti diganggu. Jika kucing menggigit saat dibelai, mungkin terjadi overstimulation - berhenti membelai dan beri ruang."}
]

# Data terstruktur untuk Jenis Kucing (cat_breeds)
breeds_data = [
    (
      "Abyssinian",
      "Tubuh ramping dan atletis dengan bulu pendek ticked (setiap helai multi-warna), telinga besar, mata almond berwarna hijau/emas, kaki panjang dan langsing. Penampilan elegan dan liar.",
      "Ethiopia (dulunya Abyssinia)",
      "Sangat aktif dan energik, sangat ingin tahu, suka memanjat tinggi, cerdas dan bisa dilatih, sosial dan suka bermain, tidak suka sendirian. Butuh banyak interaksi."
    ),
    (
      "Russian Blue",
      "Bulu abu-abu kebiruan pendek dan tebal dengan silver tips, undercoat dan topcoat sama panjang, mata hijau cemerlang, tubuh ramping dan elegan. Wajah terlihat seperti tersenyum.",
      "Rusia",
      "Pemalu dengan orang asing, loyal pada pemilik, tenang dan pendiam, cerdas dan observan, rutinitas oriented, sensitif pada perubahan. Memerlukan waktu untuk membuka diri."
    ),
    (
      "Kucing Kampung",
      "Penampilan sangat bervariasi, umumnya bertubuh sedang dengan bulu pendek. Berbagai warna dan pola. Sangat adaptif terhadap lingkungan tropis Indonesia dan Asia Tenggara.",
      "Indonesia dan Asia Tenggara",
      "Tangguh dan adaptif, cerdas dan mandiri, lincah dan aktif. Kepribadian beragam tergantung individu. Mudah beradaptasi dengan berbagai kondisi lingkungan."
    ),
    (
      "American Shorthair",
      "Tubuh medium hingga besar, berotot dan atletis, kepala bulat besar, mata bulat lebar, bulu pendek tebal. Berbagai warna dan pola, silver tabby paling populer.",
      "Amerika Serikat",
      "Easy-going dan adaptif, tidak terlalu demanding, baik dengan anak-anak dan hewan lain, playful tapi tidak hyperaktif, mandiri namun affectionate. Kucing keluarga ideal."
    ),
    (
      "Norwegian Forest Cat",
      "Kucing besar dengan bulu double coat panjang dan tebal tahan air, telinga besar dengan lynx tips, kaki besar dengan bulu di antara jari, ekor lebat. Dibuat untuk iklim dingin.",
      "Norwegia",
      "Ramah dan sosial, cerdas, atletis dan suka memanjat, mandiri tapi penyayang, sabar dengan anak-anak. Butuh waktu untuk mature (3-4 tahun)."
    ),
    (
      "Birman",
      "Bulu semi-panjang dengan color point pattern seperti Siamese, mata biru sapphire, 'sarung tangan' putih di keempat kaki yang simetris, tubuh medium berat.",
      "Myanmar (Burma), dikembangkan di Prancis",
      "Lembut dan penyayang, tidak terlalu vokal seperti Siamese, sosial dan baik dengan anak-anak, playful tapi tidak hyperaktif, suka dipeluk. Balance sempurna antara aktif dan kalem."
    )
]

# Data terstruktur untuk Penyakit (cat_diseases)
diseases_data = [
    (
      "Diare",
      "Feses cair atau lembek, buang air besar lebih sering dari biasanya, kadang disertai muntah, dehidrasi, lemas, kehilangan nafsu makan",
      "Puasa 12-24 jam (tetap berikan air), berikan makanan bland seperti ayam rebus dan nasi, pastikan hidrasi cukup. Konsultasi dokter jika berlanjut lebih dari 24 jam, ada darah dalam feses, atau kucing sangat lemas.",
      "Sedang-Tinggi"
    ),
    (
      "Muntah",
      "Mengeluarkan makanan atau cairan dari mulut, lemas, tidak mau makan, kadang disertai diare, air liur berlebihan",
      "Perhatikan frekuensi dan isi muntahan. Jika muntah hairball sesekali itu normal, berikan hairball paste. Puasa 4-6 jam lalu berikan makanan sedikit-sedikit. Konsultasi dokter jika muntah berulang, ada darah, atau kucing dehidrasi.",
      "Rendah-Tinggi"
    ),
    (
      "Infeksi Saluran Kemih (Feline Lower Urinary Tract Disease/FLUTD)",
      "Sering ke litter box tapi hanya pipis sedikit atau tidak keluar sama sekali, pipis berdarah, mengeong kesakitan saat pipis, menjilati area genital berlebihan, pipis di luar litter box",
      "SEGERA KE DOKTER HEWAN! Ini adalah kondisi darurat terutama pada kucing jantan. Dokter akan memberikan antibiotik, pain relief, dan mungkin memasang kateter. Tingkatkan asupan air, berikan makanan basah, hindari stress.",
      "Tinggi"
    ),
    (
      "Infeksi Telinga (Otitis)",
      "Menggaruk telinga terus-menerus, menggelengkan kepala, kotoran telinga berlebihan berwarna hitam/coklat, bau tidak sedap dari telinga, telinga kemerahan atau bengkak, kepala miring ke satu sisi",
      "Bawa ke dokter untuk pemeriksaan. Jangan bersihkan telinga sendiri jika sudah infeksi. Dokter akan memberikan obat tetes telinga antibiotik atau antijamur. Bersihkan telinga rutin setelah sembuh untuk pencegahan.",
      "Sedang"
    )
]

def insert_all_data():
    try:
        conn = psycopg2.connect(DB_PARAMS)
        cur = conn.cursor()
        print("🚀 Menghubungkan ke database...")

        # A. Ingest ke cat_knowledge (RAG)
        print("Memasukkan data pengetahuan (vektor)...")
        for item in knowledge_data:
            vector = embeddings_model.embed_query(item['text'])
            cur.execute(
                "INSERT INTO cat_knowledge (content, category, embedding) VALUES (%s, %s, %s)",
                (item['text'], item['cat'], vector)
            )

        # B. Ingest ke cat_breeds (Data Master)
        print("Memasukkan data jenis kucing...")
        execute_values(cur, 
            "INSERT INTO cat_breeds (name, description, origin, temperament) VALUES %s", 
            breeds_data
        )

        # C. Ingest ke cat_diseases (Data Master)
        print("Memasukkan data penyakit...")
        execute_values(cur, 
            "INSERT INTO cat_diseases (name, symptoms, treatment_suggestion, danger_level) VALUES %s", 
            diseases_data
        )

        conn.commit()
        print("✅ Semua data berhasil dimasukkan!")

    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    insert_all_data()
