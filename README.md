# Aturmation

## 📌 Deskripsi
**Aturmation** adalah aplikasi berbasis web yang dirancang untuk mempermudah pengelolaan stok barang secara real-time. Dengan fitur CRUD (Create, Read, Update, Delete) pada entitas Produk dan Kategori, aplikasi ini membantu bisnis dalam memantau stok barang, melakukan pencatatan transaksi, dan menghasilkan laporan inventaris secara efisien.

---

## 🚀 Fitur Utama
- **CRUD Produk dan Kategori:** Kelola data produk dan kategori secara lengkap.
- **Laporan Stok Barang:** Tampilkan data stok dalam bentuk tabel dan grafik.
- **Pencatatan Transaksi Barang:** Rekam pemasukan dan pengeluaran stok.
- **Notifikasi Stok Rendah:** Peringatan saat stok mencapai batas minimal.
- **Pencarian Produk Cepat:** Fitur pencarian instan berdasarkan nama atau kode produk.
- **Autentikasi dan Keamanan:** Proteksi akses menggunakan JWT.

---

## 🛠️ Teknologi yang Digunakan
### Frontend
- React JS (Vite)
- TailwindCSS
- React Router DOM
- Axios

### Backend
- Python Pyramid (RESTful API)
- PostgreSQL
- JWT (JSON Web Token)
- Unit Testing (60% Coverage)

### Version Control
- Git & GitHub

---

## 🗃️ Database Structure
```
Tabel Produk
- id (Primary Key)
- nama_produk
- kategori_id (Foreign Key)
- stok
- harga
- deskripsi

Tabel Kategori
- id (Primary Key)
- nama_kategori

Tabel Transaksi
- id (Primary Key)
- produk_id (Foreign Key)
- jumlah
- jenis_transaksi (masuk/keluar)
- tanggal_transaksi
```

---

## 🔄 API Endpoint
| Method | Endpoint            | Deskripsi                |
|---------|----------------------|--------------------------|
| GET     | `/api/products`     | Menampilkan semua produk |
| GET     | `/api/products/:id` | Menampilkan detail produk|
| POST    | `/api/products`     | Menambah produk baru     |
| PUT     | `/api/products/:id` | Mengedit data produk     |
| DELETE  | `/api/products/:id` | Menghapus produk         |

| Method | Endpoint              | Deskripsi                |
|---------|----------------------|--------------------------|
| GET     | `/api/categories`    | Menampilkan semua kategori |
| POST    | `/api/categories`    | Menambah kategori baru     |
| PUT     | `/api/categories/:id`| Mengedit data kategori     |
| DELETE  | `/api/categories/:id`| Menghapus kategori         |

---

## 🔧 Cara Menjalankan Aplikasi
1. Clone repository:
   ```bash
   git clone https://github.com/username/nim-ims.git
   cd nim-ims
   ```

2. Setup backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   python3 main.py
   ```

3. Setup frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. Buka di browser:
   ```
   http://localhost:5173
   ```

---

## 📌 Dokumentasi Tambahan
- Link Dokumentasi API: [Swagger Docs](http://localhost:8000/docs)
- Link GitHub Repository: [Aturmation](https://github.com/GhiffariIs/tugasbesar_pemrograman_web_122140189)

---

## 📞 Kontak
- Nama: [Nama Kamu]
- Email: [Email Kamu]
- GitHub: [Username GitHub Kamu]
""
