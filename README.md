# 📱 SmartPick: Prediksi Harga & Rekomendasi Smartphone

Proyek Data Mining (ST167) | Universitas Amikom Yogyakarta

---

## 📖 Deskripsi Proyek
**SmartPick** adalah aplikasi berbasis web cerdas yang dirancang untuk membantu konsumen menentukan kewajaran harga sebuah smartphone berdasarkan spesifikasi teknisnya. Seringkali, konsumen mengalami *information overload* dan kebingungan saat memilih HP. Sistem ini hadir sebagai panduan objektif untuk mencegah konsumen membayar terlalu mahal (*overpaying*).

Aplikasi ini menggunakan algoritma *Machine Learning* **Random Forest Classifier** untuk mengklasifikasikan spesifikasi input ke dalam empat rentang harga:
* 💚 **Murah** (Rp 500.000 – Rp 2.000.000)
* 💙 **Menengah** (Rp 2.000.000 – Rp 4.000.000)
* 🧡 **Mahal** (Rp 4.000.000 – Rp 7.000.000)
* 💜 **Premium** (Rp 7.000.000+)

Selain prediksi, sistem ini juga terintegrasi dengan data riil untuk menampilkan **rekomendasi produk smartphone asli** yang beredar di pasaran Indonesia sesuai dengan kelas harga hasil prediksi.

## ✨ Fitur Utama
* **Form Input Interaktif:** Antarmuka *user-friendly* yang menerjemahkan pilihan spesifikasi umum (seperti "RAM 4 GB" atau "Baterai Besar") ke dalam matriks teknis.
* **Prediksi Cerdas & Akurat:** Menggunakan model *Random Forest* yang dilatih dengan 2.000 dataset *Mobile Price Classification* dari Kaggle.
* **Tingkat Kepercayaan Model (*Confidence Score*):** Menampilkan persentase keyakinan model terhadap hasil prediksi.
* **Sistem Rekomendasi Riil:** Menampilkan rekomendasi 30 produk smartphone nyata dari berbagai merek yang relevan dengan spesifikasi dan kelas harga pengguna.

## 🛠️ Teknologi yang Digunakan
* **Bahasa Pemrograman:** Python 3
* **Machine Learning:** Scikit-Learn (Random Forest)
* **Data Manipulation:** Pandas, NumPy
* **Web Framework:** Streamlit
* **Deployment:** Launchinpad Amikom

## 🚀 Cara Menjalankan Proyek di Lokal
Jika kamu ingin menjalankan aplikasi ini di komputer lokal, ikuti langkah-langkah berikut:

1. Clone repository ini:
   ```bash
   git clone [https://github.com/USERNAME_GITHUB_KAMU/smartpick-prediksi-harga-hp.git](https://github.com/USERNAME_GITHUB_KAMU/smartpick-prediksi-harga-hp.git)

2. Masuk ke direktori proyek:
   ```bash 
   cd smartpick-prediksi-harga-hp

3. Install semua requirments libary
   ```bash
   pip install -r requirments.txt

4. Jalankan aplikasi Streamlit
   ``` bash
   streamlit run app.py

   
