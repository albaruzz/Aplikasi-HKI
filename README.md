# Klasifikasi Citra Real atau Fake

Aplikasi web sederhana (Flask) untuk mengklasifikasikan apakah sebuah gambar **Real** (asli) atau **Fake** (buatan AI), menggunakan model CNN `model/my_model21.h5`.

## Menjalankan aplikasi

Aplikasi memerlukan Python 3.12 (TensorFlow tidak mendukung Python 3.14).

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Buka http://127.0.0.1:5000. Unggah gambar lalu tekan **Klasifikasi**.

Endpoint: `POST /predict` dengan field multipart `file` -> JSON `{label, probability, confidence}`.

## Evaluasi pada dataset CIFAKE

```powershell
.\.venv\Scripts\python.exe eval_cifake.py
```

Perintah pertama mengunduh split test CIFAKE (~8 MB) dari Hugging Face ke `~/.cache/huggingface`. Referensi baseline: akurasi 93.95%, ROC-AUC 0.9861.

## Struktur

- `app.py` — server Flask (unggah -> prediksi -> hasil)
- `config.py` — konstanta bersama (preprocessing, label kelas, path model)
- `eval_cifake.py` — skrip evaluasi pada CIFAKE test
- `templates/index.html` — halaman UI (Bahasa Indonesia)
- `model/my_model21.h5` — model Keras, input 32x32x3 RGB, output sigmoid

## Pra-pemrosesan

Gambar diubah ke RGB, di-resize ke 32x32 (LANCZOS), lalu dibagi 255. Konstanta ini berada di `config.py`.
