# Kalkulator Kriptografi Berbasis Web

Aplikasi web sederhana untuk melakukan **enkripsi dan dekripsi menggunakan algoritma kriptografi klasik**.
Dibangun menggunakan **Python (Flask)** dengan antarmuka modern berbasis Bootstrap.

---

## Fitur

Aplikasi ini mendukung 5 algoritma kriptografi klasik:

* ✅ Vigenere Cipher
* ✅ Affine Cipher
* ✅ Playfair Cipher
* ✅ Hill Cipher (Matrix 2x2)
* ✅ Enigma Cipher (Versi Sederhana)

Fitur tambahan:

* Tampilan modern (Glassmorphism UI)
* Encrypt & Decrypt
* Copy hasil ke clipboard
* Validasi error sederhana
* Berbasis web (tidak perlu GUI tambahan)

---

## 🛠 Teknologi yang Digunakan

* Python 3.x
* Flask
* NumPy
* HTML5
* CSS3
* Bootstrap 5
* JavaScript

---

## Struktur Project

```
tugas-kriptografi-kalkulator/
│
├── app.py
├── README.md
└── requirements.txt (opsional)
```

---

## Cara Menjalankan Program

### 1️⃣ Clone Repository

```
git clone https://github.com/SkyzJrz/kalkulator-kriptografi-tugas
cd tugas-kriptografi-kalkulator
```

### 2️⃣ Install Dependency

```
pip install flask numpy
```

Atau jika menggunakan requirements.txt:

```
pip install -r requirements.txt
```

### 3️⃣ Jalankan Program

```
python app.py
```

### 4️⃣ Buka di Browser

```
http://127.0.0.1:5000/
```

---

## Cara Penggunaan

1. Pilih algoritma cipher dari dropdown.
2. Masukkan plaintext atau ciphertext.
3. Masukkan key sesuai format berikut:

| Cipher   | Format Key      | Contoh  |
| -------- | --------------- | ------- |
| Vigenere | Kata            | UNDIP   |
| Affine   | a,b             | 7,10    |
| Playfair | Kata            | GADJAH  |
| Hill     | 4 angka matriks | 3,3,2,5 |
| Enigma   | Angka posisi    | 3       |

4. Klik **Encrypt** atau **Decrypt**.
5. Hasil akan muncul di bagian bawah dan dapat di-copy.

---

## Penjelasan Singkat Algoritma

### 🔹 Vigenere Cipher

Menggunakan metode substitusi majemuk berbasis kata kunci.

### 🔹 Affine Cipher

Menggunakan persamaan linear:

C = (aP + b) mod 26

### 🔹 Playfair Cipher

Menggunakan matriks 5x5 dan mengenkripsi dalam pasangan huruf.

### 🔹 Hill Cipher

Menggunakan operasi perkalian matriks modulo 26.

### 🔹 Enigma Cipher

Simulasi sederhana mesin Enigma dengan rotor dan reflector.

---

## Catatan

* Program hanya memproses huruf A–Z.
* Hill Cipher membutuhkan determinan matriks relatif prima terhadap 26.
* Enigma pada aplikasi ini adalah versi sederhana (bukan simulasi historis lengkap).

---
## 👨‍💻 Author

Nama: Janottama Ale Prasetyo
NIM : 21120123140046

---
