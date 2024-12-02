import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Fungsi untuk menghitung rekomendasi
def hitung_rekomendasi():
    try:
        # Mengambil nilai dari slider
        risiko_value = slider_risiko.get()
        pengembalian_value = slider_pengembalian.get()
        jangka_waktu_value = slider_jangka_waktu.get()

        # Fungsi keanggotaan untuk risiko
        def fuzzy_membership_risiko(value):
            rendah = max(0, min(1, (5 - value) / 4))  # Nilai maksimal 5
            sedang = max(0, min((value - 3) / 2, (7 - value) / 2))  # Nilai 3-7
            tinggi = max(0, min((value - 6) / 4, 1))  # Nilai minimal 6
            return {"rendah": rendah, "sedang": sedang, "tinggi": tinggi}

        # Fungsi keanggotaan untuk pengembalian
        def fuzzy_membership_pengembalian(value):
            rendah = max(0, min(1, (5 - value) / 4))  # Nilai maksimal 5
            sedang = max(0, min((value - 3) / 2, (7 - value) / 2))  # Nilai 3-7
            tinggi = max(0, min((value - 6) / 4, 1))  # Nilai minimal 6
            return {"rendah": rendah, "sedang": sedang, "tinggi": tinggi}

        # Fungsi keanggotaan untuk jangka waktu
        def fuzzy_membership_jangka_waktu(value):
            pendek = max(0, min(1, (3 - value) / 2))  # Nilai maksimal 3 tahun
            sedang = max(0, min((value - 2) / 1, (5 - value) / 2))  # Nilai 2-5 tahun
            panjang = max(0, min((value - 4) / 2, 1))  # Nilai minimal 4 tahun
            return {"pendek": pendek, "sedang": sedang, "panjang": panjang}

        # Keanggotaan risiko, pengembalian, dan jangka waktu
        risiko_membership = fuzzy_membership_risiko(risiko_value)
        pengembalian_membership = fuzzy_membership_pengembalian(pengembalian_value)
        jangka_waktu_membership = fuzzy_membership_jangka_waktu(jangka_waktu_value)

        # Semua kombinasi aturan
        rules = [
            {"risiko": "rendah", "pengembalian": "tinggi", "jangka_waktu": "pendek", "output": "Sangat Direkomendasikan"},
            {"risiko": "rendah", "pengembalian": "tinggi", "jangka_waktu": "sedang", "output": "Direkomendasikan"},
            {"risiko": "rendah", "pengembalian": "sedang", "jangka_waktu": "pendek", "output": "Direkomendasikan"},
            {"risiko": "sedang", "pengembalian": "tinggi", "jangka_waktu": "pendek", "output": "Direkomendasikan"},
            {"risiko": "sedang", "pengembalian": "sedang", "jangka_waktu": "pendek", "output": "Perlu Pertimbangan"},
            {"risiko": "tinggi", "pengembalian": "rendah", "jangka_waktu": "panjang", "output": "Tidak Direkomendasikan"},
        ]

        # Mencari aturan terbaik
        best_rule = None
        best_similarity = 0
        
        for rule in rules:
            risiko_degree = risiko_membership[rule["risiko"]]
            pengembalian_degree = pengembalian_membership[rule["pengembalian"]]
            jangka_waktu_degree = jangka_waktu_membership[rule["jangka_waktu"]]
            similarity = min(risiko_degree, pengembalian_degree, jangka_waktu_degree)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_rule = rule
        
        # Keputusan akhir
        output = best_rule["output"] if best_rule else "Tidak Direkomendasikan"

        # Menampilkan hasil di label
        result_risiko.config(text=f"Tingkat Risiko: {risiko_value}")
        result_pengembalian.config(text=f"Potensi Pengembalian: {pengembalian_value}")
        result_jangka_waktu.config(text=f"Jangka Waktu: {jangka_waktu_value} tahun")
        result_output.config(text=f"Rekomendasi: {output}")

        # Menampilkan tombol grafik setelah perhitungan selesai
        btn_show_graph.pack(pady=10)
        btn_back.pack(pady=10)

        # Pindah ke Slide 2 untuk menampilkan hasil
        show_slide(2)
    
    except ValueError:
        # Jika input tidak valid
        result_output.config(text="Input tidak valid!")

# Fungsi untuk menampilkan slide tertentu
def show_slide(slide_number):
    if slide_number == 0:
        frame_intro.pack(pady=50)
        frame_input.pack_forget()
        frame_result.pack_forget()
        btn_show_graph.pack_forget()
        btn_back.pack_forget()
    elif slide_number == 1:
        frame_intro.pack_forget()
        frame_input.pack(pady=20)
    elif slide_number == 2:
        frame_result.pack(pady=20)
        frame_input.pack_forget()
        frame_intro.pack_forget()

# Membuat aplikasi GUI
root = tk.Tk()
root.title("Fuzzy Rekomendasi Investasi")
root.geometry("900x600")

# Komponen GUI
frame_intro = tk.Frame(root)
frame_intro.pack()
btn_start = tk.Button(frame_intro, text="Mulai", command=lambda: show_slide(1))
btn_start.pack()

frame_input = tk.Frame(root)
slider_risiko = tk.Scale(frame_input, from_=1, to=10, orient="horizontal")
slider_pengembalian = tk.Scale(frame_input, from_=1, to=10, orient="horizontal")
slider_jangka_waktu = tk.Scale(frame_input, from_=1, to=10, orient="horizontal")
slider_risiko.pack()
slider_pengembalian.pack()
slider_jangka_waktu.pack()
btn_hitung = tk.Button(frame_input, text="Hitung", command=hitung_rekomendasi)
btn_hitung.pack()

frame_result = tk.Frame(root)
result_risiko = tk.Label(frame_result)
result_pengembalian = tk.Label(frame_result)
result_jangka_waktu = tk.Label(frame_result)
result_output = tk.Label(frame_result)
result_risiko.pack()
result_pengembalian.pack()
result_jangka_waktu.pack()
result_output.pack()

btn_show_graph = tk.Button(root, text="Grafik")
btn_back = tk.Button(root, text="Kembali", command=lambda: show_slide(0))

show_slide(0)
root.mainloop()
