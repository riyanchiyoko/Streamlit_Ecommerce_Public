# E-Commerce Dashboard

Dashboard ini dirancang untuk menganalisis dataset e-commerce publik 
dan memberikan wawasan seperti kategori produk populer, penjual terbaik, dan tren penjualan bulanan.
Dashboard dibangun menggunakan **Streamlit** untuk visualisasi data interaktif.

---

## 🎯 **Fitur Utama**
1. Menampilkan **5 kategori produk terpopuler** dan **5 kategori produk dengan penjualan terendah**.
2. Analisis **5 seller dengan total nilai penjualan tertinggi di tahun 2018**.
3. Grafik garis penjualan bulanan untuk **kategori produk terpopuler**.

---

## 🛠️ **Persyaratan**
Sebelum menjalankan aplikasi, pastikan Anda sudah menginstal:
- Python >= 3.8
- Library Python berikut:
  - `streamlit`
  - `pandas`
  - `matplotlib`
  - `seaborn`

---

## 🚀 **Cara Menjalankan Dashboard**
1. **Clone repository ini** ke komputer Anda:
   ```bash
   git clone https://github.com/riyanchiyoko/Streamlit_Ecommerce_Public
2. Masuk ke folder project: 
    cd Streamlit_Ecommerce_Public
3. Buat virtual environment (opsional, tapi direkomendasikan): 
    python -m venv env
    source env/bin/activate      # Mac/Linux
    env\Scripts\activate         # Windows
4. Install dependensi yang diperlukan: 
    pip install -r requirements.txt
5. Jalankan aplikasi Streamlit: 
    streamlit run dashboard.py
6. Akses dashboard melalui browser: Setelah menjalankan perintah di atas, Anda akan melihat URL seperti: 
    Local URL: http://localhost:8501
    Buka URL tersebut di browser Anda. 
