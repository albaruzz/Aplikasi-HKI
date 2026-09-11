#!/usr/bin/env python3
"""Buku panduan CIFAKE Detector — gaya template proposal grafis.
Palet: charcoal gelap + oranye + amber, nomor bab besar, bar aksen,
pagebreak tiap BAB (disengaja), footer nomor halaman oranye.
Isi & gambar sama seperti build_guide.py, bahasa baku, tanpa sebutan HKI.
"""
import pathlib
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = pathlib.Path(__file__).parent.parent
DOC = ROOT / "docs" / "BUKU_PANDUAN_CIFAKE_Detector.docx"
LOGO = ROOT / "docs" / "logo_undip.png"
if not LOGO.exists():
    alt = pathlib.Path.home() / "Projects" / "cifake-detector" / "docs" / "logo_undip.png"
    if alt.exists():
        LOGO = alt

S_INIT_LIGHT = ROOT / "docs" / "screenshot_01_initial_light.png"
S_INIT_DARK = ROOT / "docs" / "screenshot_01_initial.png"
S_FAKE_DARK = ROOT / "docs" / "screenshot_02_FAKE.png"
S_FAKE_LIGHT = ROOT / "docs" / "screenshot_03_FAKE_light.png"
IMG = ROOT / "docs" / "image.png"
if not IMG.exists():
    IMG = ROOT / "assets" / "image.png"

DARK = RGBColor(0x1A, 0x1A, 0x1A)
ORANGE = RGBColor(0xE8, 0x5A, 0x2E)
AMBER = RGBColor(0xF2, 0xA9, 0x00)
GRAY = RGBColor(0x6B, 0x72, 0x80)
INK = RGBColor(0x1A, 0x1A, 0x1A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

BODY_FONT = "Calibri"
HEAD_FONT = "Bevan"

_bid = 0

def shade(p, fill):
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    shd.set(qn("w:val"), "clear")
    pPr.append(shd)

def bookmark(p, name):
    global _bid
    _bid += 1
    s = OxmlElement("w:bookmarkStart")
    s.set(qn("w:id"), str(_bid)); s.set(qn("w:name"), name)
    e = OxmlElement("w:bookmarkEnd")
    e.set(qn("w:id"), str(_bid)); e.set(qn("w:name"), name)
    p._p.append(s); p._p.append(e)

def hyperlink(p, text, target, color="E85A2E"):
    hl = OxmlElement("w:hyperlink")
    if target.startswith("#"):
        hl.set(qn("w:anchor"), target[1:])
    else:
        from docx.opc.constants import RELATIONSHIP_TYPE
        rid = p.part.relate_to(target, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
        hl.set(qn("r:id"), rid); hl.set(qn("w:history"), "1")
    r = OxmlElement("w:r"); rp = OxmlElement("w:rPr")
    c = OxmlElement("w:color"); c.set(qn("w:val"), color); rp.append(c)
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rp.append(u)
    r.append(rp); r.text = text; hl.append(r); p._p.append(hl)

def toc_field(p):
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve")
    it.text = ' TOC \\o "1-3" \\h \\z \\u '
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "separate")
    f3 = OxmlElement("w:fldChar"); f3.set(qn("w:fldCharType"), "end")
    for el in (f1, it, f2, f3):
        r = OxmlElement("w:r"); r.append(el); p._p.append(r)

def code(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(6)
    shade(p, "F3F4F6")
    r = p.add_run(text)
    r.font.name = "Consolas"; r.font.size = Pt(7)
    r.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
    return p

def bar(doc, color="E85A2E", space_after=8):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(space_after)
    shade(p, color)
    r = p.add_run(" ")
    r.font.size = Pt(4)
    return p

def kicker(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text.upper())
    r.bold = True; r.font.size = Pt(9); r.font.color.rgb = ORANGE; r.font.name = HEAD_FONT
    return p

def h1(doc, number, title, anchor):
    h = doc.add_heading(level=1)
    r1 = h.add_run(f"{number}  ")
    r1.bold = True; r1.font.size = Pt(20); r1.font.color.rgb = ORANGE; r1.font.name = HEAD_FONT
    r2 = h.add_run(title)
    r2.bold = True; r2.font.size = Pt(16); r2.font.color.rgb = DARK; r2.font.name = HEAD_FONT
    bookmark(h, anchor)
    bar(doc, color="F2A900", space_after=6)
    return h

def h2(doc, title, anchor):
    h = doc.add_heading(level=2)
    r1 = h.add_run("▍ ")
    r1.font.color.rgb = ORANGE; r1.font.size = Pt(12)
    r2 = h.add_run(title)
    r2.bold = True; r2.font.size = Pt(12); r2.font.color.rgb = DARK; r2.font.name = BODY_FONT
    bookmark(h, anchor)
    return h

def caption(doc, label, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(2)
    r = p.add_run(label + "  ")
    r.bold = True; r.font.size = Pt(8); r.font.color.rgb = ORANGE
    r2 = p.add_run(text)
    r2.italic = True; r2.font.size = Pt(8); r2.font.color.rgb = GRAY
    return p

def pic(doc, path, width=5.8):
    doc.add_picture(str(path), width=Inches(width))
    p = doc.paragraphs[-1]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return p

def style_table(tbl, header=True):
    tbl.style = "Light Grid Accent 1"
    if header and len(tbl.rows):
        for c in tbl.rows[0].cells:
            for pr in c.paragraphs:
                for r in pr.runs:
                    r.bold = True; r.font.color.rgb = WHITE; r.font.size = Pt(9)
            tcPr = c._tc.get_or_add_tcPr()
            shd = OxmlElement("w:shd")
            shd.set(qn("w:fill"), "E85A2E"); shd.set(qn("w:val"), "clear")
            tcPr.append(shd)

def read(p):
    try:
        return open(str(p), encoding="utf-8").read()
    except Exception:
        return ""

# ===== dokumen =====
doc = Document()
for sec in doc.sections:
    sec.top_margin = Inches(0.6); sec.bottom_margin = Inches(0.7)
    sec.left_margin = Inches(0.7); sec.right_margin = Inches(0.7)
    sec.header_distance = Inches(0.35); sec.footer_distance = Inches(0.4)

st = doc.styles["Normal"]
st.font.name = BODY_FONT; st.font.size = Pt(10)
st.paragraph_format.space_after = Pt(6); st.paragraph_format.line_spacing = 1.07
for i in (1, 2, 3):
    hs = doc.styles[f"Heading {i}"]
    hs.font.name = HEAD_FONT if i == 1 else BODY_FONT
    hs.font.color.rgb = DARK

# header kanan mungil
hdr = doc.sections[0].header
hp = hdr.paragraphs[0]; hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = hp.add_run("CIFAKE DETECTOR  •  Klasifikasi Citra Real atau Fake")
r.font.size = Pt(7); r.font.color.rgb = GRAY; r.font.name = BODY_FONT

# ===== SAMPUL ala template: blok gelap + badge oranye =====
if LOGO.exists():
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(); run.add_picture(str(LOGO), width=Inches(1.15))

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
shade(p, "1A1A1A"); p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(0)
r = p.add_run("UNIVERSITAS DIPONEGORO  •  FSM  •  DEPARTEMEN INFORMATIKA")
r.bold = True; r.font.size = Pt(8); r.font.color.rgb = WHITE; r.font.name = BODY_FONT

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
shade(p, "1A1A1A"); p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)
r = p.add_run("BUKU PANDUAN")
r.bold = True; r.font.size = Pt(11); r.font.color.rgb = RGBColor(0xF2, 0xA9, 0x00); r.font.name = HEAD_FONT

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
shade(p, "1A1A1A"); p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)
r = p.add_run("CIFAKE DETECTOR")
r.bold = True; r.font.size = Pt(30); r.font.color.rgb = WHITE; r.font.name = HEAD_FONT

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
shade(p, "1A1A1A"); p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)
r = p.add_run("Klasifikasi Citra Real atau Fake")
r.bold = True; r.font.size = Pt(14); r.font.color.rgb = RGBColor(0xF2, 0xA9, 0x00); r.font.name = BODY_FONT

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
shade(p, "1A1A1A"); p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(10)
r = p.add_run("Optimasi Klasifikasi Citra Hasil Kecerdasan Buatan Menggunakan\nConvolutional Neural Network — Model21")
r.italic = True; r.font.size = Pt(10); r.font.color.rgb = RGBColor(0xD4, 0xD4, 0xD8)

bar(doc, color="E85A2E", space_after=4)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Aplikasi Web Flask  •  CIFAKE 120.000 Citra (32×32)  •  CNN BatchNorm + Dropout 0,1")
r.font.size = Pt(8); r.font.color.rgb = GRAY
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("✦   Val Accuracy 0,9408   •   F1-Score 0,9396   •   Val Loss 0,1542   ✦")
r.bold = True; r.font.size = Pt(8); r.font.color.rgb = ORANGE

tbl = doc.add_table(rows=1, cols=2); tbl.autofit = True
c0, c1 = tbl.rows[0].cells
c0.text = "Penyusun\nHamid Albar Nurrasyid\n24060120130069"
c1.text = "Pembimbing\nDr. Helmie Arif Wibawa, S.Si., M.Cs.\nHenri Tantyoko, S.Kom., M.Kom."
for c in (c0, c1):
    for pr in c.paragraphs: pr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tcPr = c._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd"); shd.set(qn("w:fill"), "FFF3E8"); shd.set(qn("w:val"), "clear")
    tcPr.append(shd)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Semarang, 2026  •  Versi 1.0  •  CIFAKE Detector  •  http://127.0.0.1:5000")
r.font.size = Pt(7); r.font.color.rgb = GRAY

doc.add_page_break()

# ===== DAFTAR ISI (field otomatis, tanpa angka statis) =====
kicker(doc, "Navigasi")
h = doc.add_heading("Daftar Isi", level=1)
for r in h.runs: r.font.color.rgb = DARK
bar(doc, color="E85A2E", space_after=4)
p = doc.add_paragraph(); toc_field(p)
p = doc.add_paragraph()
r = p.add_run("Catatan: daftar isi di atas dihasilkan otomatis melalui field TOC. Apabila nomor halaman belum tampil, klik kanan pada daftar isi di Word/LibreOffice dan pilih Update Field > Update entire table.")
r.font.size = Pt(7); r.font.color.rgb = GRAY; r.italic = True
toc_items = [
    ("BAB 1  Latar Belakang", "#bab1"),
    ("1.1  Perkembangan Citra Sintetis", "#bab1_1"),
    ("1.2  Dataset CIFAKE", "#bab1_2"),
    ("1.3  Rumusan Masalah", "#bab1_3"),
    ("1.4  Tujuan Aplikasi", "#bab1_4"),
    ("BAB 2  Deskripsi Program", "#bab2"),
    ("2.1  Gambaran Umum", "#bab2_1"),
    ("2.2  Fitur Utama", "#bab2_2"),
    ("2.3  Arsitektur Sistem", "#bab2_3"),
    ("2.4  Struktur Proyek", "#bab2_4"),
    ("BAB 3  Pembuatan Model di Jupyter Notebook", "#bab3"),
    ("3.1  Lingkungan & Dataset", "#bab3_1"),
    ("3.2  Pra-pemrosesan & Konfigurasi", "#bab3_2"),
    ("3.3  Arsitektur Baseline & Model21", "#bab3_3"),
    ("3.4  39 Variasi & Model Terbaik", "#bab3_4"),
    ("3.5  Menyimpan & Memuat Model", "#bab3_5"),
    ("BAB 4  Interface Program & Cara Pakai", "#bab4"),
    ("4.1  Tampilan", "#bab4_1"),
    ("4.2  Alur Pakai + Contoh FAKE 99,99%", "#bab4_2"),
    ("4.3  Skenario Uji", "#bab4_3"),
    ("4.4  Akses API Flask", "#bab4_4"),
    ("BAB 5  Source Code Lengkap", "#bab5"),
    ("5.1  Backend Flask (app.py)", "#bab5_1"),
    ("5.2  Konfigurasi (config.py)", "#bab5_2"),
    ("5.3  Interface (templates/index.html)", "#bab5_3"),
    ("5.4  Evaluasi & Smoke Test", "#bab5_4"),
    ("Lampiran A  Struktur & Menjalankan", "#lampA"),
    ("Lampiran B  API Reference", "#lampB"),
]
# Nomor halaman diisi otomatis setelah pengukuran PDF (lihat TOC_NUMBERS).
# Jalankan build sekali, ukur posisi heading via pdftotext, lalu isi dict dan build final.
TOC_NUMBERS = {
    "#bab1": 3, "#bab1_1": 3, "#bab1_2": 3, "#bab1_3": 3, "#bab1_4": 3,
    "#bab2": 4, "#bab2_1": 4, "#bab2_2": 4, "#bab2_3": 4, "#bab2_4": 4,
    "#bab3": 6, "#bab3_1": 6, "#bab3_2": 6, "#bab3_3": 6, "#bab3_4": 7, "#bab3_5": 7,
    "#bab4": 8, "#bab4_1": 8, "#bab4_2": 8, "#bab4_3": 9, "#bab4_4": 9,
    "#bab5": 10, "#bab5_1": 10, "#bab5_2": 11, "#bab5_3": 11, "#bab5_4": 13,
    "#lampA": 17, "#lampB": 17,
}
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER
for text, anchor in toc_items:
    is_bab = text.startswith("BAB") or text.startswith("Lampiran")
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.left_indent = Inches(0.15 if is_bab else 0.45)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(6.4), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    hyperlink(p, text, anchor, color="1A1A1A")
    num = str(TOC_NUMBERS.get(anchor, ""))
    r = p.add_run("\t" + num)
    r.font.name = BODY_FONT; r.font.size = Pt(9)
    r.bold = is_bab; r.font.color.rgb = DARK

# ===== BAB 1 =====
doc.add_page_break()
kicker(doc, "Bab 1 — Konteks")
h1(doc, "1", "Latar Belakang", "bab1")
h2(doc, "1.1  Perkembangan Citra Sintetis dan Risiko Deepfake", "bab1_1")
doc.add_paragraph(
    "Perkembangan kecerdasan buatan generatif (GAN, Stable Diffusion) memungkinkan pembuatan citra sintetis yang sangat realistis "
    "dan sulit dibedakan dari citra asli. Manfaatnya besar bagi industri kreatif, tetapi risikonya serius: penyebaran deepfake, manipulasi media, "
    "dan ancaman terhadap validitas informasi digital (Verdoliva, 2020). Tesis ini menjawab tantangan tersebut dengan fokus pada deteksi citra FAKE versus REAL."
)
h2(doc, "1.2  Dataset CIFAKE", "bab1_2")
doc.add_paragraph(
    "CIFAKE (Bird & Lotfi, 2024) merupakan benchmark 120.000 citra berwarna berukuran 32×32 yang dirancang khusus untuk evaluasi ini: 60.000 citra REAL dari CIFAR-10 asli "
    "dan 60.000 citra FAKE hasil model generatif. Struktur direktori memisahkan data latih dan data uji serta kelas FAKE dan REAL sehingga relevan untuk klasifikasi biner. "
    "Citra FAKE sering mengandung artefak halus, tetapi secara global mirip dengan citra REAL sehingga memerlukan ekstraksi fitur hierarkis."
)
p = doc.add_paragraph()
r = p.add_run("Karakteristik CIFAKE: "); r.bold = True
p.add_run("total 120 ribu, seimbang 60 ribu berbanding 60 ribu, ukuran 32×32×3, format JPG/PNG, pra-pemrosesan MinMax /255, pengubahan ukuran LANCZOS.")
h2(doc, "1.3  Rumusan Masalah Tesis", "bab1_3")
for b in [
    "Model CNN baseline mengalami overfitting: akurasi latih tinggi, tetapi akurasi validasi stagnan dan loss validasi lebih tinggi.",
    "Diperlukan regularisasi yang tepat: dropout dan batch normalization untuk menstabilkan distribusi aktivasi dan mengurangi overfitting.",
    "Belum jelas kombinasi optimal dropout (conv/dense) dan batch normalization untuk CIFAKE.",
]:
    doc.add_paragraph(b, style="List Bullet")
h2(doc, "1.4  Tujuan Aplikasi", "bab1_4")
doc.add_paragraph(
    "Buku panduan ini beserta aplikasi web Flask membungkus hasil tesis Model21 menjadi detektor interaktif. Pengguna mengunggah citra, sistem mengonversi citra ke ruang warna RGB, "
    "mengubah ukuran menjadi 32×32 piksel dengan metode LANCZOS, melakukan normalisasi dengan pembagian nilai 255, menjalankan inferensi menggunakan model CNN my_model21.h5, "
    "dan mengembalikan label FAKE atau REAL beserta tingkat kepercayaan. Tujuannya adalah mempermudah demonstrasi, pengujian, dan dokumentasi tanpa harus menjalankan notebook secara langsung."
)
tbl = doc.add_table(rows=1, cols=3)
hdr = tbl.rows[0].cells
hdr[0].text = "Val Accuracy\n0,9408"; hdr[1].text = "Val Loss\n0,1542"; hdr[2].text = "F1-Score\n0,9396"
style_table(tbl)

# ===== BAB 2 =====
doc.add_page_break()
kicker(doc, "Bab 2 — Program")
h1(doc, "2", "Deskripsi Program", "bab2")
h2(doc, "2.1  Gambaran Umum", "bab2_1")
doc.add_paragraph(
    "CIFAKE Detector merupakan aplikasi web berbasis Flask dengan satu templat HTML dan model Keras my_model21.h5 yang mengimplementasikan Model21 dari tesis. "
    "Backend Python melayani antarmuka pengguna pada rute GET / dan endpoint POST /predict dengan field multipart file. Frontend menggunakan JavaScript murni untuk menangani "
    "fungsionalitas seret dan lepas (drag-and-drop), pratinjau citra, serta penampilan hasil. Validasi jenis berkas (png/jpg/jpeg/bmp/webp) dan batas ukuran 5 MB dilakukan dengan penanganan kesalahan dalam format JSON yang jelas."
)
h2(doc, "2.2  Fitur Utama", "bab2_2")
for f in [
    "Unggah dengan mekanisme seret dan lepas serta klik untuk memilih berkas (format JPG/PNG/JPEG/BMP/WEBP, ukuran maksimum 5 MB, pratinjau otomatis).",
    "Pratinjau citra beserta informasi nama dan ukuran berkas, tombol Klasifikasi dan Hapus Gambar.",
    "Kartu hasil: lencana FAKE (warna merah) atau REAL (warna hijau) beserta ikon, label, dan tingkat kepercayaan dalam persen.",
    "Desain responsif, kartu berlebar 460 piksel di tengah, bingkai putus-putus 1,5 piksel pada area unggah.",
    "Backend Flask: pemuatan model secara lazy, pra-pemrosesan RGB menjadi 32×32 LANCZOS lalu /255 (config.py).",
    "Endpoint POST /predict mengembalikan {label, probability, confidence} dengan ambang batas 0,5 (nilai ≥0,5 diklasifikasikan sebagai REAL).",
]:
    doc.add_paragraph(f, style="List Bullet")
h2(doc, "2.3  Arsitektur Sistem", "bab2_3")
doc.add_paragraph(
    "Klien (peramban) membuka GET / menuju templates/index.html, memilih berkas, lalu JavaScript mengirim FormData ke POST /predict. "
    "Flask memeriksa nama berkas, membuka citra dengan Pillow, melakukan pra-pemrosesan (RGB, ubah ukuran 32×32 LANCZOS, /255, expand_dims), "
    "menjalankan model Keras my_model21.h5 (Conv2D 32 3×3 relu, BatchNorm, MaxPool 2×2, Dropout 0,1, dua blok, Flatten, Dense 64 relu, Dense 1 sigmoid), "
    "menghitung probability, menetapkan label (≥0,5 Real), menghitung confidence, lalu mengembalikan JSON untuk dirender JavaScript."
)
tbl = doc.add_table(rows=4, cols=1)
tbl.rows[0].cells[0].text = "Frontend: templates/index.html (satu HTML, CSS, JS, fetch /predict)"
tbl.rows[1].cells[0].text = "Backend: app.py (Flask, GET /, POST /predict, batas 5 MB)"
tbl.rows[2].cells[0].text = "Config & Model: config.py (IMG 32, RESCALE, CLASS_0/1) ke model/my_model21.h5"
tbl.rows[3].cells[0].text = "Deploy: .venv Python 3.12, app.py ke http://127.0.0.1:5000 (TF CPU)"
style_table(tbl)
h2(doc, "2.4  Struktur Proyek", "bab2_4")
code(doc, "\n".join([
    "CIFAKE Detector/",
    "├── app.py                 # Server Flask (GET /, POST /predict)",
    "├── config.py              # IMG 32, RESCALE, MODEL_PATH, CLASS_0/1",
    "├── model/my_model21.h5    # Model Keras 32×32×3 ke sigmoid (1,1 MB)",
    "├── templates/index.html   # Antarmuka Indonesia + CSS + JS internal",
    "├── assets/image.png       # Contoh uji kucing oranye (68 KB)",
    "├── assets/screenshot-FAKE.png",
    "├── docs/                  # Panduan + screenshot + build_proposal.py",
    "├── requirements.txt       # tensorflow 2.21.0, flask 3.1.3, pillow 12.3.0",
    "├── smoke_test.py          # Pengujian unit (5 pengujian)",
    "└── eval_cifake.py         # Evaluasi uji CIFAKE 20 ribu citra",
]))
doc.add_paragraph(
    "Berkas model my_model21.h5 berukuran sekitar 1,1 MB dan dimuat secara lazy pada saat aplikasi pertama kali menerima permintaan prediksi. "
    "Seluruh konstanta pra-pemrosesan terpusat pada config.py sehingga aplikasi, skrip evaluasi, dan pengujian menggunakan nilai yang identik."
)

# ===== BAB 3 =====
doc.add_page_break()
kicker(doc, "Bab 3 — Model")
h1(doc, "3", "Pembuatan Model di Jupyter Notebook", "bab3")
h2(doc, "3.1  Lingkungan & Dataset", "bab3_1")
doc.add_paragraph(
    "Notebook Kaggle menggunakan GPU P100, Python 3.10, TensorFlow/Keras, scikit-learn, Pillow, dan matplotlib. "
    "Dataset CIFAKE dari Kaggle (real-and-ai-generated-synthetic-images) dengan direktori train dan test. "
    "Eksperimen dilakukan dengan 39 variasi untuk menemukan kombinasi Batch Normalization dan Dropout yang optimal. "
    "Notebook asli tersedia secara publik pada https://www.kaggle.com/code/hamidalbar/tugas-akhir (Versi 19, lisensi Apache 2.0)."
)
p = doc.add_paragraph()
r = p.add_run("Tautan notebook: "); r.font.size = Pt(8)
hyperlink(p, "https://www.kaggle.com/code/hamidalbar/tugas-akhir", "https://www.kaggle.com/code/hamidalbar/tugas-akhir")
r = p.add_run("  •  Lisensi Apache 2.0  •  Tesla P100, cuDNN 8.9.0")
r.font.size = Pt(7); r.font.color.rgb = GRAY; r.italic = True
code(doc, "train_dir = '/kaggle/input/cifake-real-and-ai-generated-synthetic-images/train'\ntest_dir  = '/kaggle/input/cifake-real-and-ai-generated-synthetic-images/test'")
h2(doc, "3.2  Pra-pemrosesan & Konfigurasi", "bab3_2")
doc.add_paragraph(
    "Setiap citra dimuat melalui Pillow: konversi ke RGB, pengubahan ukuran menjadi (32,32) dengan metode LANCZOS, konversi ke array NumPy float32 dan normalisasi dengan pembagian 255,0. "
    "Nilai tersebut diatur pada config.py (IMG_WIDTH=32, IMG_HEIGHT=32, RESCALE=True) dan harus identik pada saat inferensi. "
    "Tidak dilakukan augmentasi berat agar fokus tetap pada pengaruh Batch Normalization dan Dropout."
)
cfg = read(ROOT / "config.py")
if cfg: code(doc, cfg[:700])
code(doc, 'def preprocess_image(img):\n    img = img.convert("RGB")\n    img = img.resize((32,32), Image.LANCZOS)\n    arr = np.asarray(img, dtype=np.float32)\n    arr = np.expand_dims(arr, axis=0)\n    if RESCALE:\n        arr /= 255.0\n    return arr')
h2(doc, "3.3  Arsitektur Baseline & Model21", "bab3_3")
code(doc, "Sequential([\n  Input((32,32,3)),\n  Conv2D(32,3x3,relu,same)+BN+MaxPool2x2+Dropout(0.1),\n  Conv2D(32,3x3,relu,same)+BN+MaxPool2x2+Dropout(0.1),\n  Flatten(), Dense(64,relu), Dense(1,sigmoid)\n])\nAdam(lr=1e-4), loss=binary_crossentropy")
doc.add_paragraph("Baseline awal tanpa BatchNorm/Dropout mengalami overfit; penambahan BatchNorm menstabilkan aktivasi dan Dropout 0,1 mencegah ko-adaptasi.")
h2(doc, "3.4  39 Variasi & Model Terbaik", "bab3_4")
doc.add_paragraph(
    "Tesis menguji 39 variasi: dropout conv (0,1/0,2), dropout dense (0,4–0,7), dan kombinasi BatchNorm. Pelatihan 20 epoch, batch 64, StratifiedKFold 5-fold. "
    "Evaluasi meliputi accuracy, loss, precision, recall, F1, dan confusion matrix. Model21 terbaik (Conv-BN-Pool-Drop0,1 dua blok + Dense64) mencapai val acc 0,9408, val loss 0,1542, F1 0,9396."
)
tbl = doc.add_table(rows=1, cols=4)
for i, t in enumerate(["Model", "Konfigurasi", "Val Acc", "Catatan"]): tbl.rows[0].cells[i].text = t
for row in [
    ["Baseline", "Conv-Pool x2 + Dense64", "~0,89", "overfit"],
    ["Variasi 1–19", "dropout conv/dense", "0,90–0,93", "dropout saja"],
    ["Variasi 20–27", "+ BatchNorm", "0,93–0,94", "stabil"],
    ["Model21", "BN + Drop 0,1", "0,9408", "TERBAIK"],
]:
    cells = tbl.add_row().cells
    for i, v in enumerate(row): cells[i].text = v
style_table(tbl)
h2(doc, "3.5  Menyimpan & Memuat Model", "bab3_5")
code(doc, "model.save('model/my_model21.h5')  # 1,1 MB\nfrom tensorflow.keras.models import load_model\nfrom config import MODEL_PATH\nmodel = load_model(MODEL_PATH)  # dipakai get_model() di app.py")

# ===== BAB 4 =====
doc.add_page_break()
kicker(doc, "Bab 4 — Penggunaan")
h1(doc, "4", "Interface Program & Cara Pakai", "bab4")
h2(doc, "4.1  Tampilan", "bab4_1")
doc.add_paragraph(
    "Antarmuka berbahasa Indonesia baku. Kartu utama berlebar 460 piksel di tengah dengan radius 24 piksel. Header menampilkan penanda DETEKSI GAMBAR, "
    "judul Klasifikasi Citra Real atau Fake, dan subjudul instruksi unggah. Area unggah berbingkai putus-putus 1,5 piksel, pratinjau maksimum 220 piksel, "
    "tombol Klasifikasi ungu penuh, serta kartu hasil hijau (Real) atau merah (Fake)."
)
if S_INIT_DARK.exists():
    caption(doc, "Gambar 4.1", "Tampilan awal — area unggah kosong di http://127.0.0.1:5000.")
    pic(doc, S_INIT_DARK, 5.2)
h2(doc, "4.2  Alur Pakai + Contoh FAKE 99,99%", "bab4_2")
for s in [
    "1. Unggah Berkas: klik area bingkai atau seret-lepas berkas JPG/PNG/JPEG/BMP/WEBP (maksimum 5 MB). Pratinjau tampil beserta nama dan ukuran berkas.",
    "2. Klasifikasi: klik Klasifikasi. Tombol menampilkan Memproses disertai indikator putar, lalu aplikasi mengirim POST /predict.",
    "3. Hasil: kartu Hasil Prediksi tampil — lencana Fake (merah) atau Real (hijau) beserta persentase kepercayaan.",
]:
    doc.add_paragraph(s, style="List Bullet")
doc.add_paragraph(
    "Sebagai contoh, berkas assets/image.png (215×215 piksel, PNG, 68,5 KB, citra kucing oranye) menghasilkan label FAKE dengan kepercayaan 99,9997% dan probability 2,13×10⁻⁶ "
    "(ambang 0,5). Hasil tersebut merupakan inferensi langsung my_model21.h5 sehingga mencerminkan kinerja val acc 0,9408."
)
if S_FAKE_DARK.exists():
    caption(doc, "Gambar 4.2", "Hasil prediksi FAKE — lencana merah, keyakinan 96,00%.")
    pic(doc, S_FAKE_DARK, 5.2)
if IMG.exists():
    caption(doc, "Gambar 4.3", "Berkas uji assets/image.png — masukan contoh.")
    pic(doc, IMG, 2.0)
code(doc, 'curl -F file=@assets/image.png http://127.0.0.1:5000/predict\n# {"label":"Fake","probability":2.13e-06,"confidence":0.999997}')
h2(doc, "4.3  Skenario Uji", "bab4_3")
tbl = doc.add_table(rows=1, cols=3)
tbl.rows[0].cells[0].text = "Masukan"; tbl.rows[0].cells[1].text = "Respons"; tbl.rows[0].cells[2].text = "Keterangan"
for row in [
    ["Foto kucing Fake\n(assets/image.png)", "Fake 99,99%\nprob 2,13e-06", "Terdeteksi Fake, sangat yakin."],
    ["Berkas PDF/txt", "Error 400\njenis tidak didukung", "Hanya png/jpg/jpeg/bmp/webp."],
    ["Citra >5 MB", "Error 413\nmelebihi batas", "MAX_CONTENT_LENGTH 5 MB."],
    ["Citra Real CIFAR", "Real 85–95%\nprob >0,5", "Confidence = probability."],
]:
    cells = tbl.add_row().cells
    for i, v in enumerate(row): cells[i].text = v
style_table(tbl)
h2(doc, "4.4  Akses API Flask", "bab4_4")
code(doc, 'curl http://127.0.0.1:5000/   # 200 HTML\ncurl -X POST http://127.0.0.1:5000/predict -F "file=@foto.jpg"\n# {"label":"Fake","probability":0.002,"confidence":0.997}')

# ===== BAB 5 =====
doc.add_page_break()
kicker(doc, "Bab 5 — Kode")
h1(doc, "5", "Source Code Lengkap", "bab5")
h2(doc, "5.1  Backend Flask (app.py)", "bab5_1")
code(doc, read(ROOT / "app.py")[:5800] or "(tidak terbaca)")
h2(doc, "5.2  Konfigurasi (config.py)", "bab5_2")
code(doc, read(ROOT / "config.py")[:1500])
h2(doc, "5.3  Interface (templates/index.html)", "bab5_3")
code(doc, read(ROOT / "templates" / "index.html")[:4800])
doc.add_paragraph("(Potongan di atas diringkas; berkas asli 421 baris mencakup variabel CSS, JS seret-lepas, pratinjau, dan fetch /predict. Lihat berkas asli untuk lengkap.)")
h2(doc, "5.4  Evaluasi & Smoke Test", "bab5_4")
code(doc, read(ROOT / "eval_cifake.py")[:3800])
code(doc, read(ROOT / "smoke_test.py")[:2800])
code(doc, read(ROOT / "requirements.txt"))

# ===== LAMPIRAN =====
doc.add_page_break()
kicker(doc, "Lampiran A")
h1(doc, "A", "Struktur & Menjalankan", "lampA")
code(doc, "# Masuk direktori proyek\n# Python 3.12 diperlukan (TensorFlow belum dukung 3.14)\nuv python install 3.12\nuv venv --python 3.12 .venv\nuv pip install -r requirements.txt --python .venv/bin/python\n.venv/bin/python app.py  # http://127.0.0.1:5000\n.venv/bin/python smoke_test.py  # 5 pengujian OK\n.venv/bin/python eval_cifake.py  # accuracy 93,95%, ROC-AUC 0,9861")
doc.add_paragraph("Catatan: versi Python sistem adalah 3.14; gunakan .venv/bin/python (3.12). TensorFlow berjalan pada CPU; peringatan CUDA/cuInit dapat diabaikan.")
h2(doc, "Lampiran B  API Reference", "lampB")
tbl = doc.add_table(rows=1, cols=4)
tbl.rows[0].cells[0].text = "Endpoint"; tbl.rows[0].cells[1].text = "Metode"
tbl.rows[0].cells[2].text = "Respons"; tbl.rows[0].cells[3].text = "Keterangan"
for row in [
    ["/", "GET", "text/html", "Antarmuka index.html"],
    ["/predict", "POST multipart", "{label, probability, confidence}", "200 OK; 400; 413 >5MB"],
    ["(error)", "—", "{error: ...}", "Tidak ada berkas / jenis / gagal / ukuran"],
]:
    cells = tbl.add_row().cells
    for i, v in enumerate(row): cells[i].text = v
style_table(tbl)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("\n— Akhir Buku Panduan —\nCIFAKE Detector • Hamid Albar Nurrasyid 24060120130069 • Departemen Informatika, FSM, Universitas Diponegoro 2026")
r.font.size = Pt(7); r.font.color.rgb = GRAY; r.italic = True

# footer nomor halaman oranye
for sec in doc.sections:
    sec.footer.is_linked_to_previous = False
    ft = sec.footer
    if not ft.paragraphs: ft.add_paragraph()
    pf = ft.paragraphs[0]; pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.paragraph_format.space_before = Pt(6); pf.text = ""
    a = pf.add_run(); f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin"); a._r.append(f1)
    b = pf.add_run(); it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = " PAGE "; b._r.append(it)
    c = pf.add_run(); f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "separate"); c._r.append(f2)
    d = pf.add_run(); f3 = OxmlElement("w:fldChar"); f3.set(qn("w:fldCharType"), "end"); d._r.append(f3)
    for rr in pf.runs: rr.font.name = BODY_FONT; rr.font.size = Pt(8); rr.font.color.rgb = ORANGE; rr.bold = True
    e = pf.add_run("  —  CIFAKE Detector")
    e.font.name = BODY_FONT; e.font.size = Pt(7); e.font.color.rgb = GRAY

doc.save(str(DOC))
print(f"saved {DOC}")
