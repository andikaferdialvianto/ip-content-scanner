# 🌐 IP Content Scanner 🎯

Alat pemindai berbasis IP untuk mendeteksi situs **judi 🎲**, **porno 🔞**, atau **umum ✅**. Dilengkapi dengan output berwarna, lokasi geografis 🌍, dan notifikasi Telegram 📩.

---

## ✨ Fitur Unggulan
- 🎲 Deteksi situs **judi** berdasarkan keyword
- 🔞 Deteksi situs **porno** berdasarkan keyword
- ✅ Deteksi situs **umum** jika tidak terindikasi
- 🌍 Menampilkan **lokasi IP** (city, region, country)
- 🖥️ Cek port dan akses HTTP/HTTPS
- 📊 Output rapi dan berwarna di terminal
- 📩 Notifikasi ke **Telegram** (opsional)

---

## ⚙️ Cara Penggunaan

### 1️⃣ Install Dependensi

Jalankan script instalasi terlebih dahulu:

```bash
chmod +x install_dependencies.sh
./install_dependencies.sh
```

### 2️⃣ Jalankan Pemindaian

Jalankan script utama dengan daftar IP:

```bash
python3 scan_situs.py ip_list.txt
```

> 💡 Gantilah `ip_list.txt` dengan file berisi daftar IP target (1 IP per baris)

---

## 📋 Format Output

Contoh output terminal:

```
Mulai proses scanning:

Progres: 100%|████████████████████████| 50/50 [00:54<00:00,  1.10s/ip]

IP                 | Lokasi                      | Kategori       | Prot.  | Path         | Status
-------------------------------------------------------------------------------------
103.149.xx.xx      | Jakarta, ID 🌍             | ✅ situs bukan | -      | -            | ❌ Situs tidak tersedia
103.160.xx.xx      | Jakarta, ID 🌍             | ✅ situs bukan | http   | /            | ✅ Akses berhasil
103.160.xx.xx      | Jakarta, ID 🌍             | ✅ situs bukan | http   | /            | ✅ Akses berhasil
103.168.xx.xx      | Jakarta, ID 🌍             | ✅ situs bukan | -      | -            | ❌ Situs tidak tersedia
103.160.xx.xx      | Jakarta, ID 🌍             | ✅ situs bukan | http   | /            | ✅ Akses berhasil
103.215.xx.xx      | Surabaya, East Java, ID 🌍 | ✅ situs bukan | http   | /            | ✅ Akses berhasil

```

---

## 📲 Notifikasi Telegram (Opsional)

Aktifkan dengan mengisi token & chat ID:

```python
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
```

---

## 🧠 Teknologi yang Digunakan
- Python `requests`, `bs4`, `socket`, `tqdm`, `colorama`
- API lokasi dari `ipinfo.io`
- Regex keyword detection

---

## 🛡️ Catatan
- Script ini **tidak menyimpan data** ke file/database
- Proses scanning hanya berbasis konten situs yang bisa diakses publik
- Tidak mendeteksi konten yang terenkripsi atau dinamis (SPA/JS-heavy)

---

🚀 Selamat menggunakan! Semoga bermanfaat! 😎
