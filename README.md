# 🌐 Judul Aplikasi Web

Deskripsi singkat mengenai aplikasi Anda, misalnya:

> Aplikasi Web Manajemen Tugas yang memungkinkan pengguna untuk membuat, melihat, memperbarui, dan menghapus daftar tugas harian mereka. Dibangun menggunakan Python Pyramid (Backend) dan React JS (Frontend) dengan antarmuka responsif.

---

## 🚀 Fitur Aplikasi

- Autentikasi pengguna (Basic Auth)
- Operasi CRUD untuk entitas (misalnya: tugas, pengguna, produk, dll.)
- UI responsif dan modern
- Navigasi antar halaman menggunakan React Router
- State management dengan Redux Toolkit / Context API
- Komunikasi frontend-backend via Axios / Fetch

---

## ⚙️ Teknologi & Dependensi

### 🔧 Backend (Python Pyramid)
- `pyramid`
- `waitress`
- `pyramid_jinja2`
- `requests`
- `pytest` (untuk testing)
- `coverage` (untuk coverage testing)

### 🎨 Frontend (React JS)
- `react`
- `react-dom`
- `react-router-dom`
- `redux` / `@reduxjs/toolkit` / `react-redux` atau `Context API`
- `axios`
- `bootstrap` / `tailwindcss` / `@mui/material` (pilih salah satu)

---

## 🛠️ Instalasi & Menjalankan Aplikasi
[Link Repository](https://github.com/GhiffariIs/tugasbesar_pemrograman_web_122140189)

### Backend
```bash
cd backend/
python -m venv venv
source venv/bin/activate  # Untuk Linux/macOS
venv\Scripts\activate     # Untuk Windows
pip install -r requirements.txt
pserve development.ini
