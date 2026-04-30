# 🛒 Proyek Analisis Data: E-Commerce Public Dataset

**Nama:** Dini Naily Farchati  
**Email:** dini210705@gmail.com  
**ID Dicoding:** CDCC180D6X2287

---

## 📁 Struktur Direktori

```
submission/
├── dashboard/
│   ├── main_data.csv       # Dataset gabungan hasil proses cleaning & feature engineering
│   └── dashboard.py        # Aplikasi dashboard Streamlit
├── data/
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
├── notebook.ipynb          # Notebook analisis data lengkap
├── requirements.txt        # Daftar library yang digunakan
└── README.md               # Panduan ini
```

---

## 🔍 Pertanyaan Bisnis

1. **Kategori produk apa yang menghasilkan total revenue tertinggi**, dan bagaimana tren revenue bulanannya selama periode 2017–2018?
2. **Apakah durasi pengiriman berpengaruh terhadap skor review pelanggan** pada pesanan berstatus *delivered* sepanjang 2016–2018?

---

## 🚀 Cara Menjalankan Dashboard

### 1. Clone / Ekstrak Submission

Ekstrak file ZIP submission ke folder lokal Anda.

### 2. Buat Virtual Environment (Opsional tapi Disarankan)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

Dari root folder `submission/`, jalankan:

```bash
pip install -r requirements.txt
```

### 4. Jalankan Dashboard

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan otomatis terbuka di browser pada alamat `http://localhost:8501`.

---

## 📊 Fitur Dashboard

- **KPI Cards**: Total pesanan, total revenue, rata-rata durasi pengiriman, dan rata-rata skor review
- **Filter interaktif**: Filter berdasarkan tahun, kategori produk, dan rentang skor review
- **Grafik Q1**: Bar chart Top-N kategori berdasarkan revenue + line chart tren revenue bulanan
- **Grafik Q2**: Bar chart rata-rata durasi pengiriman per skor review + box plot distribusi
- **Tabel ringkasan**: Statistik deskriptif durasi pengiriman per skor review
- **Insight & Rekomendasi**: Kesimpulan dan action item hasil analisis

---

## 🛠️ Library yang Digunakan

| Library | Versi | Kegunaan |
|---------|-------|----------|
| pandas | 2.2.2 | Manipulasi data |
| numpy | 1.26.4 | Komputasi numerik |
| matplotlib | 3.9.0 | Visualisasi data |
| seaborn | 0.13.2 | Visualisasi statistik |
| streamlit | 1.35.0 | Dashboard interaktif |
