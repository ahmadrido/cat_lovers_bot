
import os
import psycopg2
from psycopg2.extras import execute_values
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import sys
  

# 1. Konfigurasi
API_KEY = "AIzaSyBrYaHxfT0QOIgqVwUfeheOxgHE3xYyvZQ"
DB_PARAMS = "postgresql://array:123456@127.0.0.1:5435/catlovers_db"

embeddings_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=API_KEY)
def get_embedding(text: str):
    response = embeddings_model.embed_query(text)
    return response

knowledge_data = [
    # Data sebelumnya...
    {"cat": "penyakit", "text": "Kucing yang lesu dan tidak mau makan bisa jadi gejala Feline Panleukopenia."},
    {"cat": "jenis", "text": "Kucing Maine Coon memiliki ciri fisik tubuh besar dan bulu tebal."},
    {"cat": "Nutrition", "text": "Makanan kering (kibble) membantu kesehatan gigi tetapi rendah hidrasi. Makanan basah sangat baik untuk hidrasi dan kesehatan saluran kemih."},
    {"cat": "Training", "text": "Letakkan litter box di tempat privat. Kucing menyukai kebersihan, jadi bersihkan bak pasir setiap hari agar mereka tidak pipis sembarangan."},
    {"cat": "Grooming", "text": "Potong kuku kucing secara rutin, namun hindari bagian 'quick' (area pink) karena mengandung saraf dan pembuluh darah."},
    {"cat": "Myths", "text": "Mitos bahwa kucing suka susu sapi adalah salah. Kebanyakan kucing dewasa laktosa intoleran dan bisa mengalami diare jika diberi susu sapi."},
    {"cat": "Behavior", "text": "Kedipan pelan (slow blink) pada kucing adalah tanda kepercayaan tinggi dan rasa sayang atau sering disebut 'cat kiss'."},
    
    # NUTRISI & MAKANAN - TAMBAHAN BARU
    {
      "cat": "Nutrisi & Makanan",
      "text": "Makanan kering untuk kucing memiliki beberapa kelebihan: lebih ekonomis dan tahan lama, membantu membersihkan gigi kucing, mudah disimpan tanpa pendingin, dan praktis untuk pemberian makan otomatis. Namun ada kekurangannya: kandungan air rendah (8-10%), dapat menyebabkan dehidrasi jika kucing kurang minum. Rekomendasi: berikan 2-3 kali sehari sesuai berat badan, pastikan air minum selalu tersedia.",
    },
    {
      "cat": "Nutrisi & Makanan",
      "text": "Makanan basah memiliki kelebihan: kandungan air tinggi (75-80%) yang membantu hidrasi kucing, lebih mudah dicerna, aroma lebih menarik untuk kucing, dan cocok untuk kucing dengan masalah ginjal. Kekurangannya: lebih mahal, cepat basi jika tidak dihabiskan, harus disimpan di kulkas setelah dibuka, dan tidak membantu membersihkan gigi. Ideal dikombinasikan dengan makanan kering untuk nutrisi seimbang.",
    },
    {
      "cat": "Nutrisi & Makanan",
      "text": "Nutrisi penting untuk kucing: Protein minimal 26% untuk kucing dewasa dan 30% untuk anak kucing. Taurin adalah asam amino esensial untuk kesehatan jantung dan mata. Lemak minimal 9% untuk energi dan kesehatan bulu. Air: kucing perlu 60ml air per kg berat badan per hari. Vitamin dan mineral seperti Vitamin A, D, E, kalsium, dan fosfor penting untuk tulang dan sistem imun.",
    },
    {
      "cat": "Nutrisi & Makanan",
      "text": "Makanan berbahaya untuk kucing yang harus dihindari: Cokelat mengandung theobromine yang beracun. Bawang merah dan bawang putih merusak sel darah merah. Susu sapi karena banyak kucing dewasa lactose intolerant. Anggur dan kismis dapat menyebabkan gagal ginjal. Kafein beracun untuk kucing. Tulang ayam dapat menyebabkan tersedak atau luka dalam.",
    },
    {
      "cat": "Nutrisi & Makanan",
      "text": "Porsi makan kucing dewasa: Berat 3-4kg membutuhkan 180-240 kalori per hari, berat 4-5kg membutuhkan 240-300 kalori, berat 5-6kg membutuhkan 300-360 kalori. Kucing hamil dan menyusui butuh 1.5-2x lipat kalori normal. Anak kucing butuh 2-3x lipat kalori per kg berat badan dibanding kucing dewasa karena masa pertumbuhan."
    },
    {
      "cat": "Nutrisi & Makanan",
      "text": "Snack dan treats untuk kucing sebaiknya tidak lebih dari 10% total kalori harian. Pilih treats yang rendah kalori dan tinggi protein. Alternatif sehat: potongan kecil ayam rebus tanpa bumbu, ikan tuna dalam air (bukan minyak), freeze-dried meat treats. Hindari treats dengan pewarna, perasa buatan, atau gula berlebihan."
    },
    {
      "cat": "Nutrisi & Makanan",
      "text": "Cara memilih makanan kucing berkualitas: Cek ingredient list, protein hewani harus di urutan pertama (chicken, fish, turkey), hindari by-products dan filler berlebihan seperti corn/wheat gluten. Perhatikan AAFCO statement yang menjamin nutrisi lengkap. Hindari makanan dengan pewarna dan perasa artificial. Sesuaikan dengan usia (kitten, adult, senior)."
    },
    {
      "cat": "Nutrisi & Makanan",
      "text": "Transisi makanan kucing harus bertahap dalam 7-10 hari untuk menghindari gangguan pencernaan. Hari 1-2: 75% makanan lama + 25% makanan baru. Hari 3-4: 50% makanan lama + 50% makanan baru. Hari 5-6: 25% makanan lama + 75% makanan baru. Hari 7-10: 100% makanan baru. Pantau feses dan nafsu makan selama transisi."
    },
    {
      "cat": "Nutrisi & Makanan",
      "text": "Raw diet (BARF - Biologically Appropriate Raw Food) untuk kucing harus dilakukan dengan hati-hati. Kelebihan: nutrisi alami, gigi lebih bersih, bulu lebih sehat. Risiko: kontaminasi bakteri (Salmonella, E.coli), ketidakseimbangan nutrisi jika tidak diformulasi dengan benar. Konsultasi dengan dokter hewan atau pet nutritionist sebelum memulai raw diet."
    },
    {
      "cat": "Nutrisi & Makanan",
      "text": "Suplemen untuk kucing sebaiknya diberikan berdasarkan kebutuhan spesifik. Omega-3 untuk kesehatan kulit dan bulu. Probiotik untuk kesehatan pencernaan. Glukosamin untuk kesehatan sendi pada senior. Lysine untuk kucing dengan riwayat herpes. JANGAN berikan suplemen manusia tanpa konsultasi dokter hewan karena dosis dan komposisi bisa berbahaya."
    },
    
    # KESEHATAN & VAKSINASI - TAMBAHAN BARU
    {
      "cat": "Kesehatan & Vaksinasi",
      "text": "Vaksinasi Tricat/F3 melindungi dari Feline Panleukopenia, Calicivirus, dan Rhinotracheitis. Jadwal: usia 8-9 minggu (pertama), 12 minggu (kedua), kemudian booster tahunan. Vaksinasi ini melindungi dari virus mematikan yang menyerang sistem pencernaan dan pernapasan kucing.",
    },
    {
      "cat": "Kesehatan & Vaksinasi",
      "text": "Vaksinasi Rabies diberikan pada usia 16 minggu dengan booster tahunan. Vaksinasi ini melindungi dari virus rabies yang mematikan dan dapat menular ke manusia. Vaksinasi rabies sangat penting terutama jika kucing sering keluar rumah atau berinteraksi dengan hewan lain.",
    },
    {
      "cat": "Kesehatan & Vaksinasi",
      "text": "Vaksinasi opsional untuk kucing: Chlamydia untuk kucing yang sering berinteraksi dengan kucing lain. Feline Leukemia Virus (FeLV) untuk kucing yang keluar rumah atau tinggal di multi-cat household. Konsultasikan dengan dokter hewan untuk menentukan vaksinasi yang diperlukan.",
    },
    {
      "cat": "Kesehatan & Vaksinasi",
      "text": "Tanda-tanda kucing sehat: mata jernih dan cerah, hidung lembab dan bersih, bulu mengkilap dan tidak rontok berlebihan, nafsu makan baik, aktif dan responsif, berat badan stabil, dan buang air normal. Perhatikan perubahan pada tanda-tanda ini untuk deteksi dini masalah kesehatan.",
    },
    {
      "cat": "Kesehatan & Vaksinasi",
      "text": "Deworming (obat cacing) untuk kucing sangat penting. Anak kucing diberikan setiap 2 minggu mulai usia 6 minggu hingga 3 bulan, lalu setiap bulan hingga usia 6 bulan. Kucing dewasa diberikan setiap 3-6 bulan tergantung gaya hidup (indoor vs outdoor). Tanda cacingan: perut buncit, berat badan turun, muntah, diare, bulu kusam."
    },
    {
      "cat": "Kesehatan & Vaksinasi",
      "text": "Pemeriksaan kesehatan rutin ke dokter hewan sebaiknya dilakukan: anak kucing setiap 3-4 minggu hingga program vaksinasi selesai, kucing dewasa sehat minimal 1x per tahun, kucing senior (7+ tahun) minimal 2x per tahun, kucing dengan kondisi kronis sesuai anjuran dokter. Check-up termasuk pemeriksaan fisik, gigi, berat badan, dan tes darah jika diperlukan."
    },
    {
      "cat": "Kesehatan & Vaksinasi",
      "text": "Sterilisasi kucing (spay/neuter) direkomendasikan pada usia 5-6 bulan sebelum pubertas pertama. Manfaat: mencegah kanker reproduksi, mengurangi perilaku marking dan aggression, mencegah kehamilan tidak diinginkan, mengurangi overpopulasi. Recovery 7-10 hari dengan perawatan luka dan menggunakan collar cone."
    },
    {
      "cat": "Kesehatan & Vaksinasi",
      "text": "Tanda kucing sakit yang memerlukan perhatian segera: tidak mau makan lebih dari 24 jam, muntah atau diare berkepanjangan, kesulitan bernapas, tidak pipis/pup lebih dari 24 jam, lemas ekstrem, kejang, perdarahan, mata atau mulut pucat (anemia), suhu tubuh di bawah 37°C atau di atas 39.5°C."
    },
    {
      "cat": "Kesehatan & Vaksinasi",
      "text": "Obesitas pada kucing adalah masalah serius. Kucing dianggap overweight jika berat 10-20% di atas ideal, obesitas jika >20%. Risiko: diabetes, penyakit jantung, arthritis, fatty liver disease. Pencegahan: porsi makan terukur, batasi treats, bermain aktif 15-30 menit per hari, timbang rutin."
    },
    {
      "cat": "Kesehatan & Vaksinasi",
      "text": "Diabetes pada kucing ditandai dengan: sering minum dan pipis berlebihan, nafsu makan meningkat tapi berat badan turun, lemas, kaki belakang lemah. Faktor risiko: obesitas, usia tua, kucing jantan. Treatment: insulin injection, diet rendah karbohidrat tinggi protein, monitoring gula darah rutin."
    },
    {
      "cat": "Kesehatan & Vaksinasi",
      "text": "Penyakit ginjal kronis (CKD) sering terjadi pada kucing senior. Gejala awal: minum banyak, pipis banyak, muntah, berat badan turun, nafsu makan berkurang. Stadium lanjut: anemia, dehidrasi, ulcer mulut. Tidak bisa disembuhkan tapi bisa di-manage dengan diet renal khusus, hidrasi, obat pendukung."
    },
    {
      "cat": "Kesehatan & Vaksinasi",
      "text": "Hyperthyroidism pada kucing senior disebabkan kelenjar tiroid overaktif. Gejala: berat badan turun drastis meski makan banyak, hyperaktif, gelisah, muntah, diare, bulu kusam. Diagnosis dengan tes darah T4. Treatment: obat methimazole, diet khusus, radioactive iodine therapy, atau operasi."
    },
    {
      "cat": "Kesehatan & Vaksinasi",
      "text": "Asma pada kucing ditandai batuk kering, mengi, kesulitan bernapas, postur membungkuk saat napas. Dipicu alergen: debu, asap rokok, parfum, serbuk sari. Treatment: inhaler bronchodilator, steroid, eliminasi trigger. Kondisi kronis yang memerlukan management seumur hidup."
    },
    
    # PERILAKU & PELATIHAN - TAMBAHAN BARU
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Perawatan litter box: Buang kotoran minimal 2x sehari. Ganti semua pasir dan cuci kotak setiap minggu. Kucing sangat bersih, jika kotak kotor mereka akan pipis sembarangan. Jangan letakkan dekat mesin cuci, area ramai, atau sudut sempit yang menakutkan.",
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Mengatasi kucing pipis sembarangan: Periksa kebersihan litter box, cek apakah ada masalah kesehatan seperti ISK, evaluasi perubahan di rumah yang bisa menyebabkan stress, tambah jumlah litter box, dan bersihkan area yang dikotori dengan enzymatic cleaner. Jangan hukum kucing karena ini kontraproduktif.",
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Alasan kucing mencakar: mengasah dan merawat kuku, menandai teritorial karena ada kelenjar di telapak kaki, peregangan otot, dan melepas stress serta energi. Ini adalah perilaku alami yang tidak bisa dihilangkan, hanya dialihkan ke tempat yang tepat.",
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Solusi mencakar furnitur: Sediakan scratching post yang kokoh dan tinggi (minimal 75cm), letakkan di area favorit kucing, gunakan bahan sisal, kardus, atau karpet. Sediakan beberapa di lokasi berbeda. Latih dengan meletakkan catnip di scratching post, beri pujian dan reward saat menggunakannya. Potong kuku setiap 2-3 minggu. Jangan pernah declawing karena merupakan amputasi yang menyakitkan.",
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Bahasa tubuh kucing - Ekor: Ekor tegak berarti senang, ramah, siap berinteraksi. Ekor mengibas cepat berarti kesal, frustrasi, jangan ganggu. Ekor di antara kaki berarti takut atau cemas. Ekor membesar seperti sikat botol berarti sangat ketakutan atau agresif.",
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Bahasa tubuh kucing - Telinga dan mata: Telinga tegak maju berarti penasaran dan waspada. Telinga ke belakang berarti marah, defensif, siap menyerang. Pupil melebar bisa berarti takut, excited, atau mode berburu.",
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Sosialisasi anak kucing: Periode kritis adalah usia 2-7 minggu. Perkenalkan berbagai orang, suara, dan pengalaman positif. Lakukan handling lembut setiap hari. Bermain dengan mainan interaktif. Sosialisasi yang baik di periode ini akan menghasilkan kucing dewasa yang percaya diri dan ramah.",
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Mendengkur pada kucing bisa memiliki arti berbeda tergantung konteks. Kucing mendengkur saat merasa senang dan nyaman, tetapi juga bisa mendengkur saat sakit atau stress sebagai mekanisme self-soothing. Beberapa penelitian menunjukkan frekuensi dengkuran (25-150 Hz) dapat membantu penyembuhan tulang dan mengurangi rasa sakit.",
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Menggigit pada kucing memiliki arti berbeda. Gigitan halus biasanya adalah bentuk main-main atau kasih sayang (love bite). Gigitan keras berarti kucing sudah mencapai batas kesabaran dan meminta untuk berhenti diganggu. Jika kucing menggigit saat dibelai, mungkin terjadi overstimulation - berhenti membelai dan beri ruang.",
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Kneading (menginjak-injak dengan kaki depan) adalah perilaku dari masa kecil saat menyusu pada induk untuk merangsang aliran susu. Kucing dewasa kneading menunjukkan mereka merasa nyaman, aman, dan mencintai Anda. Kadang disertai air liur dan dengkuran. Jika cakarnya sakit, potong kuku atau letakkan selimut tebal."
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Bunting (menggosokkan kepala/tubuh pada Anda atau benda) adalah cara kucing menandai teritorial dengan kelenjar scent di pipi, dagu, dan kepala. Ini tanda kepemilikan dan kasih sayang. Mereka 'mengklaim' Anda sebagai bagian dari territory aman mereka."
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Membawa 'hadiah' mangsa (tikus, cicak, burung) adalah naluri berburu dan cara kucing berbagi hasil buruan dengan keluarga mereka. Mereka juga mungkin mencoba 'mengajari' Anda berburu. Jangan marah atau hukum kucing - ini adalah perilaku alami. Beri pujian lalu buang dengan tenang."
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Zoomies (berlari kencang tiba-tiba) biasanya terjadi setelah buang air atau malam hari. Ini cara kucing melepas energi terpendam dan sangat normal terutama pada kucing muda. Pastikan ruangan aman tanpa benda berbahaya. Bermain aktif 15-30 menit sebelum tidur bisa mengurangi zoomies malam."
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Mengubur kotoran adalah naluri kucing untuk menyembunyikan bau dari predator. Kucing yang tidak mengubur kotorannya di litter box bisa jadi: box terlalu kecil, pasir tidak nyaman, atau perilaku dominasi. Kucing dominan kadang sengaja tidak mengubur untuk menandai teritorial."
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Tidur banyak adalah normal untuk kucing - 12-16 jam per hari, anak kucing bisa tidur 20 jam. Mereka adalah crepuscular (paling aktif saat fajar dan senja). Tidur membantu conserve energy untuk hunting. Jika kucing tiba-tiba tidur lebih lama dari biasa dan lemas, bisa jadi tanda sakit."
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Melatih kucing datang saat dipanggil: gunakan clicker atau kata konsisten, panggil nama lalu beri treat segera saat datang, mulai jarak dekat lalu jauhkan bertahap, latih 5-10 menit per hari, jangan pernah panggil untuk hal negatif (mandi, ke dokter). Sabar dan konsisten."
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Mengatasi kucing agresif: identifikasi trigger (takut, sakit, teritorial, mainan kasar), beri ruang dan jangan paksa interaksi, konsultasi dokter untuk rule out masalah medis, gunakan positive reinforcement, hindari hukuman fisik. Agresi medis (redirected, pain-induced) butuh treatment berbeda dari agresi perilaku."
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Separation anxiety pada kucing: gejala termasuk vocalization berlebihan, destructive behavior, over-grooming, tidak mau makan saat ditinggal. Solusi: buat rutinitas konsisten, tinggalkan mainan interaktif, pertimbangkan teman kucing kedua, gunakan pheromone diffuser (Feliway), latih independent play."
    },
    {
      "cat": "Perilaku & Pelatihan",
      "text": "Memperkenalkan kucing baru ke kucing lama: isolasi kucing baru di ruangan terpisah 3-7 hari, tukar scent dengan handuk atau bedding, biarkan melihat tanpa kontak (through door), pertemuan pertama supervised dan singkat, beri makan di sisi berbeda pintu tertutup, perlahan perpendek jarak. Proses bisa 2-4 minggu."
    },
    
    # PANDUAN PERAWATAN - TAMBAHAN BARU
    {
      "cat": "Panduan Perawatan",
      "text": "Menyisir bulu kucing: Untuk bulu pendek 1-2x seminggu, bulu panjang setiap hari. Gunakan sisir gigi lebar, slicker brush, atau sisir kutu. Mulai dari kepala ke ekor, berhati-hati di area sensitif. Manfaatnya: mengurangi hairball, mencegah bulu kusut, deteksi dini masalah kulit, dan bonding time dengan kucing.",
    },
    {
      "cat": "Panduan Perawatan",
      "text": "Memandikan kucing: Frekuensi setiap 4-6 minggu atau saat sangat kotor. Kucing membersihkan diri sendiri sehingga tidak perlu terlalu sering. Gunakan air hangat dan shampo khusus kucing (pH balanced). Hindari area mata, telinga, dan hidung. Bilas hingga bersih dan keringkan dengan handuk atau hair dryer suhu rendah. Mulai saat masih kecil agar terbiasa.",
    },
    {
      "cat": "Panduan Perawatan",
      "text": "Memotong kuku kucing: Lakukan setiap 2-3 minggu menggunakan gunting kuku khusus kucing. Tekan telapak lembut agar kuku keluar, potong hanya bagian putih/transparan, hindari quick (bagian pink berisi pembuluh darah). Jika berdarah gunakan styptic powder. Lakukan saat kucing rileks atau mengantuk, beri reward setelahnya.",
    },
    {
      "cat": "Panduan Perawatan",
      "text": "Kebersihan telinga kucing: Periksa setiap minggu, bersihkan jika perlu (setiap 2-4 minggu). Gunakan ear cleaner khusus kucing atau NaCl 0.9%. Teteskan ke lubang telinga, pijat pangkal telinga, biarkan kucing menggelengkan kepala, lap bagian luar dengan kapas. JANGAN masukkan cotton bud ke dalam telinga. Ke dokter jika ada kotoran berlebihan, bau tidak sedap, atau kucing sering menggaruk telinga.",
    },
    {
      "cat": "Panduan Perawatan",
      "text": "Kebersihan gigi kucing: Penting untuk mencegah karang gigi, gingivitis, dan penyakit periodontal. Sikat gigi ideal 2-3x seminggu menggunakan sikat gigi jari atau sikat kecil dengan pasta gigi khusus kucing (jangan pasta gigi manusia). Alternatif: dental treats, mainan dental, makanan kering, atau air additive. Scaling di dokter hewan setiap 1-2 tahun jika diperlukan.",
    },
    {
      "cat": "Panduan Perawatan",
      "text": "Kebersihan mata kucing: Lap kotoran mata dengan kapas basah air hangat, bersihkan dari sudut dalam ke luar. Gunakan kapas berbeda untuk setiap mata. Sedikit kotoran di sudut mata saat bangun tidur adalah normal. Tidak normal jika ada kotoran berlebihan berwarna kuning/hijau, mata merah dan berair terus, mata tertutup atau bengkak, atau selaput putih menutup mata.",
    },
    {
      "cat": "Panduan Perawatan",
      "text": "Peralatan grooming dasar untuk kucing: slicker brush untuk bulu medium-panjang, sisir logam gigi lebar dan halus, flea comb untuk deteksi kutu, gunting kuku, shampo khusus kucing pH-balanced, handuk microfiber, cotton balls, ear cleaner, sikat gigi kucing. Investasi awal tapi akan hemat biaya grooming salon."
    },
    {
      "cat": "Panduan Perawatan",
      "text": "Mat dan tangles pada bulu panjang: cegah dengan menyisir rutin setiap hari. Untuk mat kecil, gunakan detangling spray dan sisir perlahan mulai dari ujung. Mat besar/parah: potong hati-hati dengan gunting tumpul parallel dengan kulit (JANGAN tegak lurus). Mat dekat kulit atau banyak = bawa ke groomer profesional untuk shaving."
    },
    {
      "cat": "Panduan Perawatan",
      "text": "Hairball (bola bulu) adalah normal karena kucing menjilati bulu yang tertelan. Gejala: batuk kering, muntah bulu berbentuk silinder. Pencegahan: sisir rutin, hairball paste/gel 2-3x seminggu, makanan formula hairball control, tingkatkan serat. Jika kucing muntah hairball >2x seminggu atau kesulitan, konsultasi dokter."
    },
    
    # MITOS VS FAKTA - TAMBAHAN BARU
    {
      "cat": "Mitos vs Fakta",
      "text": "MITOS: Kucing selalu jatuh dengan empat kaki dan tidak pernah terluka. FAKTA: Kucing memiliki righting reflex, tapi tetap bisa terluka parah atau mati dari ketinggian. Jatuh dari lantai 2-7 paling berbahaya karena kucing tidak punya cukup waktu untuk posisi landing yang benar.",
    },
    {
      "cat": "Mitos vs Fakta",
      "text": "MITOS: Kucing tidak butuh perhatian dan mandiri total. FAKTA: Kucing butuh stimulasi mental, interaksi sosial, dan perhatian. Mereka bisa kesepian dan stress jika diabaikan. Kucing adalah hewan sosial yang membentuk ikatan dengan pemiliknya.",
    },
    {
      "cat": "Mitos vs Fakta",
      "text": "MITOS: Kucing yang dimandulkan akan jadi gemuk dan malas. FAKTA: Penambahan berat badan terjadi karena metabolisme berubah setelah sterilisasi, tapi bisa dikontrol dengan diet yang tepat dan olahraga. Manfaat sterilisasi jauh lebih besar daripada risiko obesitas yang bisa dicegah.",
    },
    {
      "cat": "Mitos vs Fakta",
      "text": "MITOS: Kucing hitam membawa sial. FAKTA: Takhayul tanpa dasar ilmiah. Di beberapa budaya seperti Jepang dan Inggris, kucing hitam justru dianggap pembawa keberuntungan. Warna bulu tidak mempengaruhi kepribadian atau membawa nasib.",
    },
    {
      "cat": "Mitos vs Fakta",
      "text": "MITOS: Kucing bisa melihat hantu atau makhluk gaib. FAKTA: Kucing memiliki pendengaran dan penglihatan superior yang mendeteksi gerakan kecil dan suara ultrasonic yang manusia tidak bisa dengar atau lihat. Mereka bisa mendengar frekuensi hingga 64 kHz (manusia hanya 20 kHz).",
    },
    {
      "cat": "Mitos vs Fakta",
      "text": "MITOS: Kucing punya 9 nyawa. FAKTA: Hanya metafora untuk ketahanan dan kelincahan kucing. Mereka tetap makhluk hidup dengan satu nyawa. Ungkapan ini muncul karena kemampuan kucing bertahan dari situasi berbahaya dan refleks yang luar biasa.",
    },
    {
      "cat": "Mitos vs Fakta",
      "text": "MITOS: Mendengkur selalu berarti kucing senang. FAKTA: Kucing juga mendengkur saat sakit, stress, atau kesakitan sebagai mekanisme self-soothing atau self-healing. Perhatikan konteks dan tanda-tanda lain untuk memahami kondisi kucing.",
    },
    {
      "cat": "Mitos vs Fakta",
      "text": "MITOS: Kucing dan anjing selalu musuhan. FAKTA: Dengan sosialisasi yang tepat sejak kecil, kucing dan anjing bisa hidup harmonis bahkan berteman baik. Banyak rumah tangga sukses memelihara kedua hewan ini bersama-sama.",
    },
    {
      "cat": "Mitos vs Fakta",
      "text": "MITOS: Whisker (kumis) kucing boleh dipotong. FAKTA: JANGAN PERNAH memotong whisker! Whisker adalah sensor penting untuk navigasi, keseimbangan, dan orientasi ruang. Memotongnya membuat kucing disorientasi dan kesulitan bergerak di ruang gelap.",
    },
    {
      "cat": "Mitos vs Fakta",
      "text": "MITOS: Kucing betina harus punya anak dulu sebelum disteril. FAKTA: TIDAK ADA manfaat kesehatan membiarkan kucing hamil sebelum sterilisasi. Justru sterilisasi sebelum heat pertama mengurangi risiko kanker payudara hingga 95%. Kehamilan malah menambah risiko komplikasi.",
    },
    {
      "cat": "Mitos vs Fakta",
      "text": "MITOS: Kucing indoor tidak butuh vaksinasi. FAKTA: Kucing indoor tetap butuh vaksinasi core (F3 minimal) karena virus bisa masuk via sepatu, pakaian, atau pengunjung. Penyakit seperti Panleukopenia sangat contagious dan bisa hidup di lingkungan berbulan-bulan.",
    },
    {
      "cat": "Mitos vs Fakta",
      "text": "MITOS: Kucing bisa vegetarian/vegan. FAKTA: Kucing adalah obligate carnivore yang WAJIB makan daging. Mereka butuh taurine, arachidonic acid, vitamin A dan D yang hanya ada di protein hewani. Diet vegetarian akan menyebabkan malnutrisi, kebutaan, masalah jantung, bahkan kematian.",
    },
    {
      "cat": "Mitos vs Fakta",
      "text": "MITOS: Kucing tidak bisa dilatih seperti anjing. FAKTA: Kucing bisa dilatih dengan metode yang tepat menggunakan positive reinforcement (clicker training). Mereka bisa belajar sit, high five, come, fetch, bahkan menggunakan toilet. Bedanya kucing lebih independent dan butuh motivasi yang tepat.",
    },
    {
      "cat": "Mitos vs Fakta",
      "text": "MITOS: Kucing hamil/menyusui tidak boleh diberi obat kutu. FAKTA: Ada produk yang aman untuk kucing hamil/menyusui seperti selamectin (Revolution). Kutu justru berbahaya untuk anak kucing karena menyebabkan anemia. Konsultasi dokter untuk produk yang aman.",
    },
    
    # LINGKUNGAN & ENRICHMENT
    {
      "cat": "Lingkungan & Enrichment",
      "text": "Cat tree dan vertical space sangat penting untuk kucing. Mereka adalah climbers alami dan merasa aman di tempat tinggi. Sediakan cat tree minimal setinggi 120cm dengan multiple levels, scratching post, dan tempat bersembunyi. Letakkan dekat jendela untuk window watching."
    },
    {
      "cat": "Lingkungan & Enrichment",
      "text": "Window perch memberikan enrichment mental untuk kucing indoor. Mereka bisa bird watching, melihat aktivitas luar, dan berjemur. Pasang bird feeder di luar jendela untuk entertainment. Pastikan jendela aman dengan screen/pengaman agar kucing tidak jatuh."
    },
    {
      "cat": "Lingkungan & Enrichment",
      "text": "Mainan interaktif untuk kucing: puzzle feeders untuk stimulasi mental, feather wands untuk interactive play, laser pointer (akhiri dengan tangible toy agar tidak frustrasi), catnip toys, motorized toys, crinkle balls. Rotasi mainan setiap minggu agar tidak bosan."
    },
    {
      "cat": "Lingkungan & Enrichment",
      "text": "Catnip (Nepeta cataria) mengandung nepetalactone yang memicu euphoria pada 70-80% kucing. Efeknya: rolling, rubbing, hyperaktif, vocal. Berlangsung 5-15 menit lalu ada refractory period 30-60 menit. Aman dan tidak addictive. Kitten di bawah 6 bulan dan 20-30% kucing tidak bereaksi."
    },
    {
      "cat": "Lingkungan & Enrichment",
      "text": "Hiding spots penting untuk kucing agar merasa aman saat stress atau butuh me-time. Sediakan cardboard boxes, cat caves, paper bags (tanpa handle), atau area di bawah tempat tidur. Kucing butuh 'safe zone' untuk decompress dari stimulasi berlebihan."
    },
    {
      "cat": "Lingkungan & Enrichment",
      "text": "Rumus litter box: jumlah kucing + 1. Jadi untuk 2 kucing butuh 3 litter box. Letakkan di area berbeda, bukan semua di satu ruangan. Ukuran box minimal 1.5x panjang tubuh kucing. Hindari covered box kecuali kucing memang prefer privacy."
    },
    {
      "cat": "Lingkungan & Enrichment",
      "text": "Jenis litter yang populer: clumping clay (paling umum, mudah dibersihkan), silica gel/crystal (absorbsi tinggi, tahan bau), natural/biodegradable (corn, wheat, paper - eco friendly). Hindari scented litter karena bisa mengganggu kucing. Depth pasir 5-7cm. Transisi litter bertahap."
    },
    {
      "cat": "Lingkungan & Enrichment",
      "text": "Catio (cat patio) adalah outdoor enclosure aman untuk kucing menikmati udara segar tanpa risiko. Bisa berupa window box kecil atau area besar di halaman. Sediakan perches, plants aman (cat grass, spider plant), scratching post, dan akses mudah dari dalam rumah."
    },
    {
      "cat": "Lingkungan & Enrichment",
      "text": "Tanaman aman untuk kucing yang bisa ditanam indoor: cat grass (wheatgrass, oatgrass), spider plant, Boston fern, African violet, bamboo, prayer plant, areca palm. Tanaman membantu enrichment dan cat grass membantu pencernaan/hairball."
    },
    {
      "cat": "Lingkungan & Enrichment",
      "text": "Tanaman BERACUN untuk kucing yang harus dihindari: lilies (SANGAT beracun, gagal ginjal), aloe vera, pothos, philodendron, dieffenbachia, peace lily, sago palm, tulips, daffodils, azalea, oleander. Gejala: muntah, diare, air liur berlebih, lethargy. Segera ke dokter jika tertelan."
    },
    
    # SITUASI DARURAT & FIRST AID
    {
      "cat": "Situasi Darurat",
      "text": "P3K dasar untuk kucing yang harus ada di rumah: termometer digital, gunting tumpul, pinset, kasa steril, perban, plester medis, betadine/antiseptic, saline solution, sarung tangan sekali pakai, selimut, carrier, nomor telepon dokter hewan 24 jam dan klinik emergensi terdekat."
    },
    {
      "cat": "Situasi Darurat",
      "text": "Cara mengukur suhu tubuh kucing: gunakan termometer digital di rectal (anus). Suhu normal 38-39.2°C. Di bawah 37°C = hypothermia (emergency), di atas 39.5°C = demam. Oleskan petroleum jelly di ujung thermometer, masukkan 2-3cm, tunggu hingga berbunyi."
    },
    {
      "cat": "Situasi Darurat",
      "text": "Tanda dehidrasi pada kucing: gusi kering dan lengket, skin tent test (kulit tidak cepat kembali saat dicubit), mata cekung, lemas, nafas cepat. Dehidrasi ringan: beri air/elektrolit. Dehidrasi sedang-berat: SEGERA ke dokter untuk IV fluids. Bisa fatal jika tidak ditangani."
    },
    {
      "cat": "Situasi Darurat",
      "text": "Mengatasi kucing tersedak: buka mulut dan cek apakah ada benda asing yang terlihat, jika ya tarik keluar dengan pinset/jari. Jika tidak terlihat JANGAN mengorek. Heimlich maneuver untuk kucing: letakkan tangan di bawah rib cage, tekan firm ke atas 5x. Segera ke dokter."
    },
    {
      "cat": "Situasi Darurat",
      "text": "Keracunan pada kucing - gejala umum: air liur berlebih, muntah, diare, tremor, kejang, kesulitan bernapas, perubahan pupil. JANGAN induce vomiting tanpa instruksi dokter. Identifikasi racun jika mungkin, hubungi pet poison control atau dokter SEGERA. Setiap menit penting."
    },
    {
      "cat": "Situasi Darurat",
      "text": "Luka/pendarahan pada kucing: luka minor - bersihkan dengan saline, apply betadine, tutup kasa steril. Pendarahan aktif - tekan luka dengan kasa 5-10 menit, elevate area jika memungkinkan, jangan angkat kasa untuk cek (biarkan clot terbentuk). Pendarahan tidak berhenti = emergency ke dokter."
    },
    {
      "cat": "Situasi Darurat",
      "text": "Heatstroke/heat exhaustion pada kucing: gejala panting berat, drooling, kemerahan gusi, vomiting, collapse. IMMEDIATE ACTION: pindah ke tempat dingin, kompres air dingin (bukan es) di ketiak/paha, kipas anginkan, beri air jika sadar. Suhu >40°C bisa menyebabkan organ failure - EMERGENCY ke dokter."
    },
    {
      "cat": "Situasi Darurat",
      "text": "Hypothermia pada kucing: gejala shivering, lemas, suhu <37°C, shallow breathing. Warming protocol: pindah ke tempat hangat, bungkus selimut/handuk hangat, heating pad suhu rendah (bungkus handuk), warm water (not hot) di sekitar tubuh. Warm gradually, terlalu cepat berbahaya. Monitor suhu."
    },
    {
      "cat": "Situasi Darurat",
      "text": "Kejang pada kucing: TETAP TENANG, jauhkan dari tangga/benda berbahaya, jangan restraint atau masukkan apapun ke mulut, catat durasi kejang, dim lights/quiet environment. Kejang >5 menit atau cluster seizures = EMERGENCY. After seizure: biarkan recovery dengan tenang, sediakan air."
    },
    
    # REPRODUKSI & BREEDING
    {
      "cat": "Reproduksi",
      "text": "Kucing betina (queen) mencapai sexual maturity usia 5-9 bulan, bisa lebih cepat pada breed tertentu. Heat cycle (estrus) 7-10 hari, jika tidak kawin akan repeat setiap 2-3 minggu saat musim kawin. Tanda heat: vocal, rolling, postur mating, agitated, minta keluar rumah."
    },
    {
      "cat": "Reproduksi",
      "text": "Kucing jantan (tom) mencapai sexual maturity 6-8 bulan. Tanda maturity: spraying urine dengan bau menyengat, marking teritorial, vocal, aggression dengan jantan lain, mencoba kawin. Sterilisasi sebelum perilaku ini muncul lebih mudah menghentikan kebiasaan marking."
    },
    {
      "cat": "Reproduksi",
      "text": "Masa kehamilan kucing 63-67 hari (rata-rata 65 hari). Tanda hamil: nipples pink dan membesar (3 minggu), perut membesar (4-5 minggu), nafsu makan meningkat, nesting behavior menjelang lahir. Ultrasound bisa deteksi kehamilan 2-3 minggu, X-ray minggu ke-6 untuk hitung anak."
    },
    {
      "cat": "Reproduksi",
      "text": "Kucing betina hamil butuh makanan kitten formula (lebih tinggi kalori dan protein) mulai minggu ke-4 kehamilan. Porsi meningkat 25-50%. Berikan free choice feeding. Tambah kalsium dari makanan (bukan suplemen kecuali diresepkan). Lanjutkan kitten food selama menyusui."
    },
    {
      "cat": "Reproduksi",
      "text": "Persiapan kelahiran kucing: sediakan birthing box di tempat tenang dan hangat, lapisi towels/blankets bersih, siapkan handuk tambahan, heating pad, timbangan, sarung tangan, gunting steril, dental floss (untuk umbilical cord), nomor dokter emergency. Jangan ganggu kecuali ada komplikasi."
    },
    {
      "cat": "Reproduksi",
      "text": "Tanda-tanda persalinan kucing: restless dan nesting (24-48 jam sebelum), suhu tubuh turun <37.8°C (12-24 jam sebelum), vocalization, menolak makan, membersihkan area genital, contractions terlihat. Stage 1: 6-12 jam, Stage 2: 30-60 menit per kitten, total bisa 6-12 jam."
    },
    {
      "cat": "Reproduksi",
      "text": "Komplikasi kelahiran yang butuh bantuan dokter SEGERA: contractions kuat >60 menit tanpa kitten lahir, kitten terlihat di jalan lahir >10 menit tapi tidak keluar, pendarahan berlebihan, ibu sangat lemas/collapse, interval antar kitten >4 jam padahal masih ada di dalam, discharge hijau/hitam berbau busuk."
    },
    {
      "cat": "Reproduksi",
      "text": "Perawatan anak kucing baru lahir: pastikan semua bernapas dan bersuara, cek umbilical cord tidak berdarah, timbang setiap hari (harus naik 10-15g/hari), pastikan semua menyusu (colostrum vital 24 jam pertama), jaga suhu ruangan 29-32°C minggu pertama. Ibu biasanya handle semuanya."
    },
    {
      "cat": "Reproduksi",
      "text": "Hand-raising anak kucing yatim: formula khusus kitten (bukan susu sapi), bottle feeding setiap 2-3 jam termasuk malam (newborn), stimulasi buang air dengan kapas basah hangat setelah feeding, jaga warm dengan heating pad suhu rendah, monitor berat badan ketat. Sangat demanding dan risky."
    },
    {
      "cat": "Reproduksi",
      "text": "Timeline perkembangan anak kucing: 1-2 minggu mata mulai buka, 2-3 minggu telinga buka dan mulai explore, 3-4 minggu mulai berjalan goyah, 4 minggu mulai makan solid food, 6-8 minggu fully weaned, 8-12 minggu siap adopsi, 4-6 bulan baby teeth ganti permanent teeth."
    },
    
    # SENIOR CAT CARE (7+ tahun)
    {
      "cat": "Perawatan Kucing Senior",
      "text": "Kucing dianggap senior mulai usia 7 tahun, geriatric di atas 11 tahun. Perubahan yang terjadi: metabolisme melambat, activity level menurun, sendi kaku (arthritis), gigi memburuk, fungsi organ menurun (ginjal, jantung), sistem imun lemah, cognitive decline (dementia kucing)."
    },
    {
      "cat": "Perawatan Kucing Senior",
      "text": "Diet untuk kucing senior: protein berkualitas tinggi tapi fosfor rendah (lindungi ginjal), kalori lebih rendah jika kurang aktif (cegah obesitas), atau lebih tinggi jika susah maintain weight, tekstur lebih lembut untuk gigi sensitif, omega-3 untuk sendi dan cognitive function, antioksidant untuk sistem imun."
    },
    {
      "cat": "Perawatan Kucing Senior",
      "text": "Arthritis/joint pain pada senior kucing: gejala subtle - tidak melompat tinggi lagi, kesulitan masuk litter box, grooming berkurang terutama area belakang, bergerak lebih lambat, postur bungkuk. Management: supplement glucosamine/chondroitin, pain medication, low entry litter box, ramps/steps, soft bedding."
    },
    {
      "cat": "Perawatan Kucing Senior",
      "text": "Cognitive Dysfunction Syndrome (CDS) pada kucing senior mirip Alzheimer: gejala disorientation (tersesat di rumah sendiri), perubahan sleep-wake cycle, decreased interaction, vocalization di malam hari, toileting accidents. Management: environmental enrichment, routine konsisten, supplements (omega-3, SAMe), medication jika severe."
    },
    {
      "cat": "Perawatan Kucing Senior",
      "text": "Modifikasi rumah untuk kucing senior: litter box dengan pinggir rendah atau tanpa tutup, food/water di beberapa lokasi mudah diakses, ramps ke tempat favorit, heated bed untuk arthritis, night lights untuk vision menurun, non-slip surfaces, pastikan semua kebutuhan di satu level (tidak perlu naik tangga)."
    },
    {
      "cat": "Perawatan Kucing Senior",
      "text": "Health screening untuk kucing senior harus lebih frequent: physical exam 2x per tahun minimal, complete blood panel (CBC, chemistry) yearly untuk deteksi dini organ dysfunction, urinalysis untuk check kidney function, blood pressure check (hipertensi umum pada senior), thyroid check (T4), dental exam."
    },
    {
      "cat": "Perawatan Kucing Senior",
      "text": "Tanda kucing senior perlu perhatian medis: berat badan turun atau naik drastis, perubahan drinking/urination, nafsu makan berubah signifikan, vomiting/diarrhea frequent, perubahan perilaku mendadak, hiding lebih sering, vocalization berlebihan terutama malam, mobility issues, confusion/disorientation."
    },
    {
      "cat": "Perawatan Kucing Senior",
      "text": "Quality of life assessment untuk kucing senior: apakah masih menikmati aktivitas favorit, level pain (scale 1-10), masih makan dan minum well, grooming diri, mobility adequate, lebih banyak good days vs bad days. Konsultasi dokter untuk diskusi quality of life dan end-of-life care jika diperlukan."
    }
]

# BREEDS DATA - TAMBAHAN BARU
breeds_data = [
        {
      "name": "Persia",
      "description": "Bulu panjang lebat dan mewah, wajah pesek (flat face) dengan hidung pendek, mata bulat besar, tubuh cobby dan kompak. Memerlukan grooming intensif setiap hari untuk mencegah matting. Berbagai warna tersedia.",
      "origin": "Iran (Persia)",
      "temperament": "Tenang dan manja, suka tempat yang nyaman dan tidak berisik, affectionate tapi tidak terlalu demanding, cocok untuk apartment, gentle dan tidak agresif. Kucing lap cat sejati."
    },
    {
      "name": "Maine Coon",
      "description": "Salah satu ras terbesar dengan berat bisa mencapai 8-10kg, bulu panjang dan tebal, telinga besar dengan lynx tips, ekor panjang lebat, tufts bulu di antara jari kaki. Adaptif dengan cuaca dingin.",
      "origin": "USA (Maine)",
      "temperament": "Ramah dan cerdas, sering disebut 'gentle giant', sosial dengan manusia dan hewan lain, playful hingga dewasa, vokal dengan chirping sounds khas, suka air. Dog-like personality."
    },
    {
      "name": "Bengal",
      "description": "Corak bulu totol atau marble seperti leopard liar, coat mengkilap dengan glitter effect, tubuh atletis dan berotot, kaki belakang lebih panjang, telinga kecil rounded. Penampilan exotic dan wild.",
      "origin": "USA (hybrid Asian Leopard Cat x Domestic)",
      "temperament": "Sangat aktif dan energik, cerdas dan curious, suka air (beberapa suka berenang), butuh banyak stimulasi mental dan fisik, athletic jumper dan climber, vokal dan demanding. Bukan untuk pemula."
    },
    {
      "name": "Siamese",
      "description": "Mata biru safir yang mencolok, pola warna point (seal, blue, chocolate, lilac) di wajah, telinga, kaki dan ekor, tubuh ramping dan elegan, kepala wedge-shaped, telinga besar. Color-point gene temperature sensitive.",
      "origin": "Thailand (dulunya Siam)",
      "temperament": "Vokal dan talkative (akan 'bercakap-cakap' dengan pemilik), setia dan sangat sosial, demanding attention, intelligent, tidak suka ditinggal sendirian, membentuk ikatan kuat dengan satu orang."
    },
    {
      "name": "Ragdoll",
      "description": "Mata biru cemerlang, bulu semi-panjang halus dan lembut, color-point pattern seperti Siamese, tubuh besar dan berat (bisa 7-9kg), 'lemas' seperti boneka kain (ragdoll) saat digendong. Lambat mature (3-4 tahun).",
      "origin": "USA (California)",
      "temperament": "Sangat penyabar dan gentle, santai dan docile, lembut dengan anak-anak, tidak agresif sama sekali, suka digendong dan dipeluk, low energy, cocok untuk indoor. Kucing terapi ideal."
    },
    {
      "name": "British Shorthair",
      "description": "Pipi tembem (chubby cheeks) khas, bulu pendek sangat padat dan plush seperti beludru, wajah bulat dengan mata bulat besar, tubuh stocky dan muscular. Blue (gray) paling populer, tapi banyak warna lain.",
      "origin": "Inggris (Great Britain)",
      "temperament": "Mandiri dan tidak clingy, tenang dan easy-going, setia pada keluarga, toleran dengan anak-anak, tidak terlalu playful saat dewasa, dignified demeanor. Low maintenance personality."
    },
    {
      "name": "Sphynx",
      "description": "Kucing tanpa bulu (hairless) dengan kulit berkerut dan hangat saat disentuh, telinga sangat besar, mata lebar, tulang pipi menonjol, tubuh berotot. Butuh perawatan kulit khusus (mandi rutin).",
      "origin": "Kanada",
      "temperament": "Sangat manja dan butuh perhatian konstan, energik dan playful, extroverted dan sosial, suka kehangatan (akan selalu cari tempat hangat atau pelukan), intelligent, clownish personality."
    },
    {
      "name": "Scottish Fold",
      "description": "Telinga terlipat ke depan dan ke bawah (folded ears) akibat mutasi genetik, wajah bulat seperti burung hantu, mata bulat besar, tubuh medium rounded. Ada juga Scottish Straight (telinga normal) dari breeding yang sama.",
      "origin": "Skotlandia",
      "temperament": "Ramah dan sweet-natured, tenang dan tidak mudah stress, mudah beradaptasi dengan lingkungan baru, baik dengan anak-anak dan hewan lain, loyal, moderate activity level."
    },
    {
      "name": "Angora",
      "description": "Bulu halus, panjang dan silky tanpa undercoat (mudah dirawat), tubuh ramping, panjang dan elegan, ekor seperti bulu boa panjang, mata bisa berbeda warna (odd-eyed), telinga besar pointed.",
      "origin": "Turki (Turkish Angora)",
      "temperament": "Lincah dan atletis, cerdas dan problem-solver, suka berinteraksi dan bermain, vokal, assertive dan bisa bossy, suka air, energik dan butuh mental stimulation. Kucing yang 'punya pendapat'."
    },
    {
      "name": "Munchkin",
      "description": "Kaki pendek karena mutasi genetik alami (bukan breeding selektif), tubuh mungil tapi proportional, bulu bisa pendek atau panjang, berbagai warna. Controversial breed karena isu kesehatan tulang belakang.",
      "origin": "USA",
      "temperament": "Suka bermain dan playful, lincah meski kaki pendek, penuh rasa ingin tahu, friendly dan outgoing, tidak terganggu dengan keterbatasan fisiknya, suka mengumpulkan benda kecil berkilau."
    },
    {
      "name": "Abyssinian",
      "description": "Tubuh ramping dan atletis dengan bulu pendek ticked (setiap helai multi-warna), telinga besar, mata almond berwarna hijau/emas, kaki panjang dan langsing. Penampilan elegan dan liar.",
      "origin": "Ethiopia (dulunya Abyssinia)",
      "temperament": "Sangat aktif dan energik, sangat ingin tahu, suka memanjat tinggi, cerdas dan bisa dilatih, sosial dan suka bermain, tidak suka sendirian. Butuh banyak interaksi."
    },
    {
      "name": "Russian Blue",
      "description": "Bulu abu-abu kebiruan pendek dan tebal dengan silver tips, undercoat dan topcoat sama panjang, mata hijau cemerlang, tubuh ramping dan elegan. Wajah terlihat seperti tersenyum.",
      "origin": "Rusia",
      "temperament": "Pemalu dengan orang asing, loyal pada pemilik, tenang dan pendiam, cerdas dan observan, rutinitas oriented, sensitif pada perubahan. Memerlukan waktu untuk membuka diri."
    },
    {
      "name": "Kucing Kampung",
      "description": "Penampilan sangat bervariasi, umumnya bertubuh sedang dengan bulu pendek. Berbagai warna dan pola. Sangat adaptif terhadap lingkungan tropis Indonesia dan Asia Tenggara.",
      "origin": "Indonesia dan Asia Tenggara",
      "temperament": "Tangguh dan adaptif, cerdas dan mandiri, lincah dan aktif. Kepribadian beragam tergantung individu. Mudah beradaptasi dengan berbagai kondisi lingkungan."
    },
    {
      "name": "American Shorthair",
      "description": "Tubuh medium hingga besar, berotot dan atletis, kepala bulat besar, mata bulat lebar, bulu pendek tebal. Berbagai warna dan pola, silver tabby paling populer.",
      "origin": "Amerika Serikat",
      "temperament": "Easy-going dan adaptif, tidak terlalu demanding, baik dengan anak-anak dan hewan lain, playful tapi tidak hyperaktif, mandiri namun affectionate. Kucing keluarga ideal."
    },
    {
      "name": "Norwegian Forest Cat",
      "description": "Kucing besar dengan bulu double coat panjang dan tebal tahan air, telinga besar dengan lynx tips, kaki besar dengan bulu di antara jari, ekor lebat. Dibuat untuk iklim dingin.",
      "origin": "Norwegia",
      "temperament": "Ramah dan sosial, cerdas, atletis dan suka memanjat, mandiri tapi penyayang, sabar dengan anak-anak. Butuh waktu untuk mature (3-4 tahun)."
    },
    {
      "name": "Birman",
      "description": "Bulu semi-panjang dengan color point pattern seperti Siamese, mata biru sapphire, 'sarung tangan' putih di keempat kaki yang simetris, tubuh medium berat.",
      "origin": "Myanmar (Burma), dikembangkan di Prancis",
      "temperament": "Lembut dan penyayang, tidak terlalu vokal seperti Siamese, sosial dan baik dengan anak-anak, playful tapi tidak hyperaktif, suka dipeluk. Balance sempurna antara aktif dan kalem."
    },
    {
      "name": "Devon Rex",
      "description": "Bulu pendek keriting dan lembut, telinga sangat besar, mata lebar, wajah elf-like, tubuh ramping berotot, tulang pipi tinggi. Terlihat sangat unik dan alien-like.",
      "origin": "Inggris (Devon)",
      "temperament": "Sangat playful dan aktif, suka loncat ke bahu pemilik, cerdas dan mischievous, sosial dan butuh perhatian, tidak suka sendirian, loyal seperti anjing."
    },
    {
      "name": "Oriental Shorthair",
      "description": "Tubuh panjang ramping seperti Siamese tapi berbagai warna solid tanpa pointing, telinga sangat besar, mata almond, kepala wedge-shaped. Lebih dari 300 variasi warna dan pola.",
      "origin": "Thailand/USA (dikembangkan)",
      "temperament": "Sangat vokal dan talkative, demanding attention, intelligent, sosial dan suka mengikuti pemilik kemana-mana, energetic, tidak cocok ditinggal sendirian lama."
    },
    {
      "name": "Burmese",
      "description": "Tubuh compact dan muscular, berat untuk ukurannya, bulu pendek mengkilap, mata emas cemerlang, rounded head. Coat warna rich solid (sable, champagne, blue, platinum).",
      "origin": "Myanmar (Burma)/USA",
      "temperament": "Sangat affectionate dan people-oriented, playful hingga tua, vokal tapi lebih soft dari Siamese, intelligent, suka involved dalam aktivitas keluarga, cocok dengan anak-anak."
    },
    {
      "name": "Exotic Shorthair",
      "description": "Wajah flat seperti Persia tapi bulu pendek, tubuh cobby dan solid, mata bulat besar, hidung pesek. Seperti 'Persia versi lazy' karena low maintenance.",
      "origin": "USA",
      "temperament": "Tenang dan gentle, affectionate, tidak terlalu demanding, playful tapi tidak hyperaktif, loyal, cocok untuk apartment. Personality Persia dengan kemudahan perawatan shorthair."
    },
    {
      "name": "Tonkinese",
      "description": "Hybrid Burmese-Siamese, tubuh medium, aqua/green eyes unik, coat mink pattern (cross antara solid dan pointed), muscular namun elegan.",
      "origin": "Kanada/USA",
      "temperament": "Sosial dan extroverted, vokal tapi tidak sevokal Siamese, playful dan aktif, sangat people-oriented, intelligent, cocok dengan anak-anak dan hewan lain."
    },
    {
      "name": "Chartreux",
      "description": "Bulu abu-abu solid tebal dan woolly, mata copper/orange mencolok, tubuh muscular dan robust, senyum khas karena struktur wajah, kaki relatif pendek.",
      "origin": "Prancis",
      "temperament": "Tenang dan gentle, tidak banyak vokal (kadang disebut mime cat), observant, loyal pada satu orang, adaptif, baik dengan anak-anak, independent tapi affectionate."
    }
]

# DISEASES DATA - TAMBAHAN BARU
diseases_data = [
    {
      "name": "Flu Kucing (Upper Respiratory Infection)",
      "symptoms": "Bersin berulang, demam, mata berair dan merah, hidung meler (discharge bening atau kental), lemas, nafsu makan menurun, mulut bernapas jika hidung tersumbat parah",
      "treatment_suggestion": "Isolasi dari kucing lain, berikan nutrisi extra dan makanan berbau kuat untuk stimulasi nafsu makan, bersihkan discharge mata/hidung rutin, humidifier untuk melembabkan udara, konsultasi dokter untuk antibiotik jika ada infeksi sekunder",
      "danger_level": "Sedang - bisa berbahaya pada anak kucing atau kucing dengan sistem imun lemah"
    },
    {
      "name": "Jamur/Ringworm (Dermatofitosis)",
      "symptoms": "Kulit merah dan iritasi, bulu rontok dalam pola melingkar/bulat (pitak), kulit bersisik atau berkerak, gatal ringan hingga sedang, lesi biasanya di wajah, telinga, atau kaki",
      "treatment_suggestion": "Salep antijamur topical (miconazole, clotrimazole), oral antifungal untuk kasus luas (itraconazole, griseofulvin), isolasi kucing, desinfeksi lingkungan dan peralatan, jemur matahari pagi. Treatment 6-12 minggu sampai kultur negatif",
      "danger_level": "Rendah - zoonotic (bisa menular ke manusia), sangat contagious tapi tidak fatal"
    },
    {
      "name": "Feline Panleukopenia (Parvo Kucing)",
      "symptoms": "Muntah parah, diare berdarah dengan bau busuk, lesu total dan dehidrasi cepat, demam tinggi (>40°C) lalu turun drastis, hilang nafsu makan total, posisi hunched karena nyeri perut",
      "treatment_suggestion": "EMERGENCY - hospitalisasi dengan IV fluids agresif, anti-nausea medication, antibiotik broad-spectrum untuk cegah sepsis, nutritional support, isolasi ketat. Vaksinasi rutin F3/F4 adalah pencegahan terbaik",
      "danger_level": "SANGAT TINGGI - mortality rate 90% pada kitten tanpa treatment, sangat contagious, virus bisa hidup di lingkungan >1 tahun"
    },
    {
      "name": "Feline Calicivirus (FCV - Flu Kucing)",
      "symptoms": "Sariawan/ulcer painful di mulut dan lidah, hidung meler, air liur berlebih, mata berair dan merah, bersin, demam, lemas, limping syndrome (arthritis sementara) pada beberapa strain",
      "treatment_suggestion": "Supportive care, soft food atau food warmer untuk stimulasi makan, pain relief untuk ulcer mulut, antibiotik jika infeksi sekunder, isolasi. Vaksinasi rutin F3/F4 dan jaga kebersihan lingkungan untuk pencegahan",
      "danger_level": "Sedang - bisa severe pada kitten, beberapa strain sangat virulent, carrier seumur hidup"
    },
    {
      "name": "Rabies",
      "symptoms": "Perubahan perilaku drastis (agresif atau terlalu jinak), takut air (hydrophobia), air liur berlebih dan berbusa, kesulitan menelan, kelumpuhan progresif dimulai dari belakang, kejang, disorientasi",
      "treatment_suggestion": "TIDAK ADA TREATMENT - fatal 100% setelah gejala muncul. PENCEGAHAN: vaksinasi rabies wajib mulai 16 minggu dan booster tahunan. Jika digigit hewan suspect rabies, segera ke dokter untuk post-exposure prophylaxis",
      "danger_level": "SANGAT TINGGI - FATAL, zoonotic dan bisa menular ke manusia, wajib dilaporkan ke authorities"
    },
    {
      "name": "Feline Immunodeficiency Virus (FIV - AIDS Kucing)",
      "symptoms": "Stadium awal: demam, pembesaran kelenjar getah bening. Stadium lanjut: berat badan turun progresif, gusi meradang kronis (gingivitis), infeksi berulang (respiratory, skin, urinary), diare kronis, coat kusam",
      "treatment_suggestion": "TIDAK ADA CURE. Management: keep indoor only untuk hindari stress dan infeksi, nutrisi berkualitas tinggi, treatment cepat untuk infeksi sekunder, antiviral (interferon omega), immune support supplements. Hindari perkelahian (transmisi via deep bite wounds)",
      "danger_level": "Sedang hingga Tinggi - penyakit kronis, kucing bisa hidup bertahun-tahun dengan care yang baik, tidak menular ke manusia"
    },
    {
      "name": "FIP (Feline Infectious Peritonitis)",
      "symptoms": "Wet form: perut membesar berisi cairan (ascites), kesulitan bernapas jika cairan di dada. Dry form: gangguan neurologis (ataxia, seizures), eye problems (uveitis), organ granulomas. Kedua form: demam tidak respon antibiotik, lemas, weight loss",
      "treatment_suggestion": "Traditionally fatal, tapi sekarang ada antiviral (GS-441524) yang menunjukkan hasil promising. Supportive care: drainage cairan, steroid, nutritional support. Pencegahan: minimalkan stress, kebersihan litter box ketat, hindari overcrowding",
      "danger_level": "SANGAT TINGGI - historically fatal, prognosis sangat poor meski dengan treatment baru"
    },
    {
      "name": "Ear Mites (Otodectes cynotis - Kutu Telinga)",
      "symptoms": "Gatal hebat di telinga (menggaruk terus-menerus), menggelengkan kepala frequent, kotoran telinga hitam kering seperti bubuk kopi, bau dari telinga, telinga merah dan iritasi, luka di telinga dari garukan",
      "treatment_suggestion": "Pembersihan telinga dengan ear cleaner, obat tetes telinga anti-parasitic (selamectin, moxidectin), bisa juga spot-on treatment (Revolution). Treat semua hewan di rumah bersamaan. Treatment 3-4 minggu untuk kill semua life cycle",
      "danger_level": "Rendah - sangat umum terutama pada kitten, mudah diobati, tapi sangat contagious antar kucing"
    },
    {
      "name": "Ringworm (Dermatophytosis - duplikat, lihat Jamur/Ringworm di atas)",
      "symptoms": "Bulu rontok melingkar (circular patches/pitak), kulit bersisik dan kemerahan, kadang gatal, lesi kering berkerak, bisa menyebar ke seluruh tubuh jika tidak diobati",
      "treatment_suggestion": "Sama seperti Jamur/Ringworm - antifungal topical dan oral, isolasi, desinfeksi lingkungan, jaga kelembapan kulit, rutin jemur matahari pagi (UV membantu kill fungal spores)",
      "danger_level": "Rendah - zoonotic, sangat menular tapi tidak fatal, butuh kesabaran untuk treatment"
    },
    {
      "name": "Toxoplasmosis",
      "symptoms": "Banyak kucing asymptomatic. Jika bergejala: demam, lemas, nafsu makan turun, sesak napas atau napas cepat, mata merah (uveitis), diare, jaundice, gangguan neurologis (jarang)",
      "treatment_suggestion": "Antibiotik (clindamycin) untuk 2-4 minggu. Pencegahan: hindari daging mentah, jaga kebersihan litter box (buang kotoran <24 jam sebelum oocysts menjadi infective), wash hands setelah handling litter. Penting untuk wanita hamil",
      "danger_level": "Rendah untuk kucing sehat - berbahaya untuk immunocompromised dan wanita hamil (zoonotic)"
    },
    {
      "name": "Chlamydia (Chlamydophila felis)",
      "symptoms": "Mata bengkak, merah, dan berair (conjunctivitis) yang kronis dan persisten, discharge mata kental, squinting, biasanya mulai satu mata lalu spread ke mata lain, mild sneezing, jarang severe",
      "treatment_suggestion": "Antibiotik topical eye ointment (tetracycline) dan/atau oral antibiotik (doxycycline) minimal 4 minggu. Isolasi dari kucing lain. Vaksinasi F4 (contains Chlamydia) untuk pencegahan di multi-cat household",
      "danger_level": "Rendah - jarang fatal, tapi sangat mengganggu dan bisa kronis jika tidak diobati tuntas"
    },
    {
      "name": "Scabies (Notoedric Mange)",
      "symptoms": "Gatal hebat dan intense scratching, kerak tebal dan crusty di kulit terutama telinga, wajah, dan leher, hair loss di area affected, kulit menebal, lesi bisa spread ke tubuh, self-trauma dari garukan",
      "treatment_suggestion": "Obat tetes tengkuk anti-parasitic (selamectin, moxidectin) setiap 2 minggu untuk 3-4 kali, lime sulfur dips, isolasi dari hewan lain, cuci semua bedding. Treat semua hewan kontak. Zoonotic tapi self-limiting di manusia",
      "danger_level": "Rendah hingga Sedang - sangat menular dan uncomfortable, tapi responsif terhadap treatment"
    },
    {
      "name": "Diare",
      "symptoms": "Feses cair atau lembek, buang air besar lebih sering dari biasanya, kadang disertai muntah, dehidrasi, lemas, kehilangan nafsu makan",
      "treatment_suggestion": "Puasa 12-24 jam (tetap berikan air), berikan makanan bland seperti ayam rebus dan nasi, pastikan hidrasi cukup. Konsultasi dokter jika berlanjut lebih dari 24 jam, ada darah dalam feses, atau kucing sangat lemas.",
      "danger_level": "Sedang hingga Tinggi - bisa menyebabkan dehidrasi berbahaya terutama pada anak kucing"
    },
    {
      "name": "Muntah",
      "symptoms": "Mengeluarkan makanan atau cairan dari mulut, lemas, tidak mau makan, kadang disertai diare, air liur berlebihan",
      "treatment_suggestion": "Perhatikan frekuensi dan isi muntahan. Jika muntah hairball sesekali itu normal, berikan hairball paste. Puasa 4-6 jam lalu berikan makanan sedikit-sedikit. Konsultasi dokter jika muntah berulang, ada darah, atau kucing dehidrasi.",
      "danger_level": "Rendah hingga Tinggi - tergantung penyebab dan frekuensi"
    },
    {
      "name": "Infeksi Saluran Kemih (Feline Lower Urinary Tract Disease/FLUTD)",
      "symptoms": "Sering ke litter box tapi hanya pipis sedikit atau tidak keluar sama sekali, pipis berdarah, mengeong kesakitan saat pipis, menjilati area genital berlebihan, pipis di luar litter box",
      "treatment_suggestion": "SEGERA KE DOKTER HEWAN! Ini adalah kondisi darurat terutama pada kucing jantan. Dokter akan memberikan antibiotik, pain relief, dan mungkin memasang kateter. Tingkatkan asupan air, berikan makanan basah, hindari stress.",
      "danger_level": "TINGGI - bisa fatal dalam 24-48 jam jika tidak ditangani, terutama pada kucing jantan"
    },
    {
      "name": "Infeksi Telinga (Otitis)",
      "symptoms": "Menggaruk telinga terus-menerus, menggelengkan kepala, kotoran telinga berlebihan berwarna hitam/coklat, bau tidak sedap dari telinga, telinga kemerahan atau bengkak, kepala miring ke satu sisi",
      "treatment_suggestion": "Bawa ke dokter untuk pemeriksaan. Jangan bersihkan telinga sendiri jika sudah infeksi. Dokter akan memberikan obat tetes telinga antibiotik atau antijamur. Bersihkan telinga rutin setelah sembuh untuk pencegahan.",
      "danger_level": "Sedang - jika tidak diobati bisa menyebabkan kerusakan permanen pada pendengaran"
    },
    {
      "name": "Conjunctivitis (Radang Mata)",
      "symptoms": "Mata merah dan bengkak, discharge mata berlebihan (berair, kuning, atau hijau), mata menyipit atau tertutup, menggosok mata dengan kaki, selaput mata (third eyelid) terlihat menonjol",
      "treatment_suggestion": "Bersihkan discharge dengan kapas basah air hangat. Dokter akan memberikan eye drops antibiotik atau antiviral tergantung penyebab. Isolasi dari kucing lain jika infeksius. Jangan gunakan obat mata manusia.",
      "danger_level": "Sedang - bisa menyebar ke kucing lain dan menyebabkan kerusakan kornea jika tidak diobati"
    },
    {
      "name": "Kutu (Fleas)",
      "symptoms": "Garuk-garuk berlebihan, gigit/lick area tertentu terus menerus, flea dirt (kotoran kutu seperti titik hitam) di bulu, bulu rontok karena over-grooming, kulit iritasi merah, pada infestasi berat bisa anemia",
      "treatment_suggestion": "Gunakan spot-on treatment (fipronil, selamectin) setiap bulan, obati semua hewan di rumah bersamaan, vacuum rumah dan cuci bedding dengan air panas, spray lingkungan jika perlu. Konsistensi penting karena siklus hidup kutu 3 bulan.",
      "danger_level": "Rendah hingga Sedang - bisa menyebabkan anemia pada anak kucing, tapeworm, dan alergi kutu"
    },
    {
      "name": "Cacing (Worms)",
      "symptoms": "Perut buncit tapi tubuh kurus, muntah (kadang ada cacing), diare, berat badan turun, bulu kusam, scooting (menggesek pantat ke lantai), cacing terlihat di feses atau anus, nafsu makan meningkat tapi tidak naik berat",
      "treatment_suggestion": "Deworming dengan obat broad-spectrum dari dokter hewan (praziquantel, pyrantel). Ulangi sesuai jadwal (biasanya 2-4 minggu kemudian). Rutin deworming setiap 3-6 bulan untuk pencegahan. Jaga kebersihan litter box.",
      "danger_level": "Rendah hingga Sedang - bisa menyebabkan malnutrisi, anemia, dan masalah pertumbuhan terutama pada anak kucing"
    },
    {
      "name": "Stomatitis (Radang Gusi dan Mulut)",
      "symptoms": "Gusi merah dan bengkak, bau mulut sangat busuk, air liur berlebihan (kadang berdarah), kesulitan makan atau menolak makan, penurunan berat badan, pawing at mouth, tidak grooming",
      "treatment_suggestion": "SEGERA ke dokter. Treatment: scaling gigi, antibiotik, pain medication, anti-inflammatory. Kasus severe mungkin perlu pencabutan gigi. Diet soft food, dental care rutin. Bisa kondisi kronis yang butuh management jangka panjang.",
      "danger_level": "Sedang hingga Tinggi - sangat painful, bisa menyebabkan malnutrisi, dan sulit disembuhkan total"
    },
    {
      "name": "Feline Herpesvirus (FHV-1)",
      "symptoms": "Mata berair dan ulcer kornea, hidung tersumbat dan bersin, demam, lemas, nafsu makan turun, ulcer di lidah, infeksi sekunder bakteri. Bisa dormant dan kambuh saat stress.",
      "treatment_suggestion": "Supportive care: lembabkan udara dengan humidifier, bersihkan discharge mata/hidung, warming food untuk aroma, lysine supplement. Dokter beri antiviral (famciclovir) dan antibiotik jika ada infeksi sekunder. Isolasi dari kucing lain.",
      "danger_level": "Sedang - bisa menjadi carrier seumur hidup, kambuh saat stress, komplikasi bisa severe terutama pada kitten"
    },
    {
      "name": "Feline Leukemia Virus (FeLV)",
      "symptoms": "Berat badan turun progresif, gusi pucat (anemia), infeksi berulang, pembesaran kelenjar getah bening, diare kronis, kesulitan bernapas, masalah reproduksi. Gejala muncul bertahap.",
      "treatment_suggestion": "TIDAK ADA CURE. Treatment supportive: boost sistem imun, obati infeksi sekunder, nutrisi berkualitas, kurangi stress, indoor only. Vaksinasi untuk pencegahan (kucing outdoor atau multi-cat). Test semua kucing baru sebelum introduce.",
      "danger_level": "TINGGI - penyakit fatal, harapan hidup berkurang signifikan, sangat contagious ke kucing lain"
    },
    {
      "name": "Fatty Liver Disease (Hepatic Lipidosis)",
      "symptoms": "Tidak mau makan sama sekali >2-3 hari, jaundice (mata dan gusi kuning), muntah, lemas ekstrem, penurunan berat badan cepat, air liur berlebih, kepala menunduk ke bawah",
      "treatment_suggestion": "EMERGENCY! Ke dokter SEGERA. Treatment: force feeding via feeding tube, IV fluids, supplements (carnitine, taurine, vitamin E), treat underlying cause. Prognosis baik jika treatment agresif dimulai cepat. Recovery bisa 6-8 minggu.",
      "danger_level": "SANGAT TINGGI - bisa fatal jika tidak segera diobati, terjadi pada kucing overweight yang tiba-tiba tidak makan"
    },
    {
      "name": "Cardiomyopathy (Hypertrophic/Dilated)",
      "symptoms": "Kesulitan bernapas (open mouth breathing), napas cepat saat istirahat, lemas dan tidak aktif, syncope (pingsan), kaki belakang tiba-tiba lumpuh (saddle thrombus), gusi biru/pucat",
      "treatment_suggestion": "SEGERA ke dokter! Diagnosis: X-ray, echocardiogram, EKG. Treatment: diuretik, ACE inhibitors, beta-blockers, anticoagulant (cegah blood clots). Diet rendah sodium. Monitor ketat. Kondisi kronis yang butuh medication seumur hidup.",
      "danger_level": "SANGAT TINGGI - bisa sudden death, saddle thrombus sangat painful dan sering fatal"
    },
    {
      "name": "Penyakit Ginjal Kronis (CKD)",
      "symptoms": "Minum air berlebihan, pipis banyak dan sering, nafsu makan menurun, muntah, berat badan turun, bulu kusam, mulut berbau, lemas, dehidrasi, ulcer mulut (stadium lanjut)",
      "treatment_suggestion": "TIDAK BISA DISEMBUHKAN tapi bisa di-manage. Treatment: diet renal prescription (rendah protein, fosfor), fluid therapy (subQ di rumah atau IV di klinik), phosphate binders, anti-nausea medication, blood pressure medication. Monitor rutin.",
      "danger_level": "TINGGI - progressive disease, common pada senior, memerlukan management seumur hidup"
    },
    {
      "name": "Hyperthyroidism",
      "symptoms": "Berat badan turun drastis meski makan banyak, hyperactive/restless, vomiting dan diarrhea, coat kusam, minum banyak, heart rate cepat, aggression atau perubahan perilaku",
      "treatment_suggestion": "Diagnosis: blood test (elevated T4). Treatment options: medication (methimazole) seumur hidup, prescription diet (y/d), radioactive iodine therapy (cure tapi mahal), surgical thyroidectomy. Monitor thyroid level dan kidney function.",
      "danger_level": "Sedang hingga Tinggi - jika tidak diobati bisa menyebabkan heart disease dan hipertensi"
    },
    {
      "name": "Diabetes Mellitus",
      "symptoms": "Minum air sangat banyak, pipis berlebihan (litter box basah terus), nafsu makan meningkat tapi berat turun, lemas, kaki belakang lemah (neuropathy), coat kusam",
      "treatment_suggestion": "Diagnosis: blood glucose test, fructosamine. Treatment: insulin injection 2x sehari, diet rendah karbo tinggi protein (wet food lebih baik), home glucose monitoring, exercise teratur. Beberapa kucing bisa remission dengan diet ketat.",
      "danger_level": "Tinggi - butuh commitment besar dari owner, komplikasi bisa severe (DKA, neuropathy), tapi manageable"
    },
    {
      "name": "Pancreatitis",
      "symptoms": "Muntah, tidak mau makan, nyeri perut (postur hunched), lemas, dehidrasi, diare, demam, breathing cepat. Gejala bisa subtle atau severe.",
      "treatment_suggestion": "Diagnosis: fPLI blood test, ultrasound. Treatment: hospitalisasi dengan IV fluids, anti-nausea, pain management, nutritional support (feeding tube jika perlu). Diet rendah lemak setelah recovery. Bisa akut atau kronis.",
      "danger_level": "Sedang hingga Tinggi - bisa life-threatening jika severe, sering co-occur dengan IBD dan liver disease"
    },
    {
      "name": "Inflammatory Bowel Disease (IBD)",
      "symptoms": "Diare kronis, muntah intermittent, berat badan turun progresif, nafsu makan berubah-ubah, coat kusam, kadang darah atau mucus di feses, lethargy",
      "treatment_suggestion": "Diagnosis: biopsy via endoscopy atau surgery. Treatment: novel protein atau hydrolyzed diet, immunosuppressive drugs (prednisolone), vitamin B12 injection, probiotics. Trial and error untuk menemukan diet yang cocok. Management jangka panjang.",
      "danger_level": "Sedang - kondisi kronis yang butuh management seumur hidup, bisa progress ke lymphoma"
    },
    {
      "name": "Lymphoma (Kanker Kelenjar Getah Bening)",
      "symptoms": "Tergantung lokasi - GI lymphoma: muntah, diare, weight loss. Mediastinal: kesulitan napas. Renal: gagal ginjal. Pembesaran kelenjar getah bening, lemas, nafsu makan turun.",
      "treatment_suggestion": "Diagnosis: biopsy, imaging. Treatment: chemotherapy (multiple drug protocol), prednisone. Prognosis bervariasi tergantung type dan lokasi. GI lymphoma prognosis lebih baik. Palliative care jika tidak respon chemo.",
      "danger_level": "SANGAT TINGGI - kanker paling umum pada kucing, prognosis guarded hingga poor tergantung type"
    },
    {
      "name": "Urolithiasis (Batu Saluran Kemih)",
      "symptoms": "Sama seperti FLUTD - sering ke litter box, hematuria (pipis berdarah), straining to urinate, crying saat pipis, licking genital area, pipis di luar box, complete obstruction = emergency",
      "treatment_suggestion": "Diagnosis: urinalysis, X-ray, ultrasound. Treatment tergantung jenis batu: struvite = prescription diet (s/d, c/d) bisa dissolve, calcium oxalate = butuh surgery. Cegah recurrence dengan diet khusus dan tingkatkan water intake.",
      "danger_level": "Sedang hingga SANGAT TINGGI - obstruction complete adalah emergency yang bisa fatal dalam 48 jam"
    },
    {
      "name": "Acne Kucing (Feline Acne)",
      "symptoms": "Blackheads (komedo) di dagu dan bibir bawah, kemerahan, bengkak, kadang infeksi sekunder dengan pustules, gatal, hair loss di area dagu",
      "treatment_suggestion": "Bersihkan dagu dengan antiseptic wipes atau benzoyl peroxide 2-3x seminggu, ganti plastic food bowl ke stainless steel atau ceramic, jaga kebersihan bowl. Kasus severe: antibiotik topical/oral, anti-inflammatory. Bisa kambuh.",
      "danger_level": "Rendah - lebih cosmetic issue, tapi infeksi sekunder bisa painful"
    },
    {
      "name": "Alergi (Makanan/Lingkungan)",
      "symptoms": "Gatal berlebihan terutama wajah, leher, telinga, over-grooming sampai bulu rontok, kulit merah dan iritasi, ear infections berulang, kadang GI signs (vomiting, diarrhea untuk food allergy)",
      "treatment_suggestion": "Identifikasi allergen: food trial (novel protein 8-12 minggu) untuk food allergy, eliminasi environmental triggers. Treatment: antihistamine, steroid (short-term), immunotherapy, omega-3 supplements. Flea control ketat untuk flea allergy.",
      "danger_level": "Rendah hingga Sedang - tidak life-threatening tapi sangat uncomfortable, butuh detective work untuk find trigger"
    }
]

def to_pgvector(vec: list) -> str:
    return "[" + ",".join(map(str, vec)) + "]"


def insert_all_data():
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(DB_PARAMS)
        cur = conn.cursor()
        print("🚀 Menghubungkan ke database...")

        # A. Ingest ke cat_knowledge (RAG)
        print(f"Memasukkan {len(knowledge_data)} data pengetahuan (vektor)...")
        success_count = 0
        for idx, item in enumerate(knowledge_data, 1):
            try:
                print(f"  [{idx}/{len(knowledge_data)}] Generating embedding for: {item['text'][:50]}...")
                vector = get_embedding(item['text'])
                
                if not vector:
                    print(f"  ⚠️ Skipping item {idx} - empty embedding")
                    continue
                
                pg_vector = to_pgvector(vector)

                cur.execute(
                    "INSERT INTO cat_knowledge (content, category, embedding) VALUES (%s, %s, %s::vector)",
                    (item['text'], item['cat'], pg_vector)
                )

                success_count += 1
                print(f"  ✓ Success")
            except Exception as e:
                print(f"  ❌ Failed to insert item {idx}: {e}")
                continue
        
        print(f"✅ Inserted {success_count}/{len(knowledge_data)} knowledge items")

        # B. Ingest ke cat_breeds (Data Master)
        print(f"Memasukkan {len(breeds_data)} data jenis kucing...")
        breeds_values = [
        (
            b["name"],
            b["description"],
            b["origin"],
            b["temperament"]
        )
        for b in breeds_data
        ]

        execute_values(
            cur,
            "INSERT INTO cat_breeds (name, description, origin, temperament) VALUES %s",
            breeds_values
        )

        print("✅ Breeds data inserted")

        # C. Ingest ke cat_diseases (Data Master)
        print(f"Memasukkan {len(diseases_data)} data penyakit...")
        diseases_values = [
        (
            d["name"],
            d["symptoms"],
            d["treatment_suggestion"],
            d["danger_level"]
        )
        for d in diseases_data
        ]

        execute_values(
            cur,
            "INSERT INTO cat_diseases (name, symptoms, treatment_suggestion, danger_level) VALUES %s",
            diseases_values
        )

        print("✅ Diseases data inserted")

        conn.commit()
        print("\n🎉 Semua data berhasil dimasukkan ke database!")
        print(f"   - Knowledge entries: {success_count}")
        print(f"   - Cat breeds: {len(breeds_data)}")
        print(f"   - Cat diseases: {len(diseases_data)}")

    except Exception as e:
        print(f"\n❌ Terjadi kesalahan: {e}")
        if conn:
            conn.rollback()
        sys.exit(1)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            print("\n📊 Koneksi database ditutup")

if __name__ == "__main__":
    print("="*60)
    print("CatLovers Bot - Data Ingestion Tool")
    print("="*60)
    insert_all_data()
