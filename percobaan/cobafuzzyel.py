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
            rendah = max(0, min(1, (30 - value) / 30))  # Nilai maksimal 30
            sedang = max(0, min((value - 10) / 20, (50 - value) / 20))  # Nilai 10-50
            tinggi = max(0, min((value - 40) / 10, 1))  # Nilai minimal 40
            return {"rendah": rendah, "sedang": sedang, "tinggi": tinggi}

        # Fungsi keanggotaan untuk pengembalian
        def fuzzy_membership_pengembalian(value):
            rendah = max(0, min(1, (20 - value) / 20))  # Nilai maksimal 20
            sedang = max(0, min((value - 5) / 15, (35 - value) / 15))  # Nilai 5-35
            tinggi = max(0, min((value - 30) / 10, 1))  # Nilai minimal 30
            return {"rendah": rendah, "sedang": sedang, "tinggi": tinggi}

        # Fungsi keanggotaan untuk jangka waktu
        def fuzzy_membership_jangka_waktu(value):
            pendek = max(0, min(1, (1 - value) / 1))  # Nilai maksimal 1 tahun
            sedang = max(0, min((value - 0.5) / 0.5, (2 - value) / 0.5))  # Nilai 0.5-2 tahun
            panjang = max(0, min((value - 1.5) / 0.5, 1))  # Nilai minimal 1.5 tahun
            return {"pendek": pendek, "sedang": sedang, "panjang": panjang}

        # Keanggotaan risiko, pengembalian, dan jangka waktu
        risiko_membership = fuzzy_membership_risiko(risiko_value)
        pengembalian_membership = fuzzy_membership_pengembalian(pengembalian_value)
        jangka_waktu_membership = fuzzy_membership_jangka_waktu(jangka_waktu_value)

        # Aturan fuzzy
        rules = [
            {"risiko": "rendah", "pengembalian": "tinggi", "jangka_waktu": "pendek", "output": "Sangat Direkomendasikan"},
            {"risiko": "rendah", "pengembalian": "sedang", "jangka_waktu": "pendek", "output": "Direkomendasikan"},
            {"risiko": "sedang", "pengembalian": "tinggi", "jangka_waktu": "pendek", "output": "Direkomendasikan"},
            {"risiko": "tinggi", "pengembalian": "tinggi", "jangka_waktu": "pendek", "output": "Perlu Pertimbangan"},
            {"risiko": "rendah", "pengembalian": "tinggi", "jangka_waktu": "panjang", "output": "Perlu Pertimbangan"},
            {"risiko": "tinggi", "pengembalian": "rendah", "jangka_waktu": "panjang", "output": "Tidak Direkomendasikan"},
        ]

        # Cari aturan dengan keanggotaan tertinggi
        best_rule = None
        best_similarity = 0  # Tingkat keanggotaan tertinggi
        
        for rule in rules:
            risiko_degree = risiko_membership[rule["risiko"]]
            pengembalian_degree = pengembalian_membership[rule["pengembalian"]]
            jangka_waktu_degree = jangka_waktu_membership[rule["jangka_waktu"]]
            similarity = min(risiko_degree, pengembalian_degree, jangka_waktu_degree)  # Derajat similaritas
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_rule = rule
        
        # Output kategori berdasarkan aturan terbaik
        if best_rule:
            output = best_rule["output"]
        else:
            output = "Tidak ada hasil"

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
        # Jika input tidak valid, tampilkan pesan error
        result_risiko.config(text="Masukkan nilai yang valid!")
        result_pengembalian.config(text="Masukkan nilai yang valid!")
        result_jangka_waktu.config(text="Masukkan nilai yang valid!")

# Fungsi untuk menampilkan slide tertentu
def show_slide(slide_number):
    if slide_number == 0:
        # Menampilkan Slide 0 (Halaman Pertama)
        frame_intro.pack(pady=50)
        frame_input.pack_forget()
        frame_result.pack_forget()
        btn_show_graph.pack_forget()
        btn_back.pack_forget()
    elif slide_number == 1:
        # Menampilkan Slide 1
        frame_intro.pack_forget()
        frame_input.pack(pady=20)
        btn_hitung.pack(pady=20)
        frame_result.pack_forget()
    elif slide_number == 2:
        # Menampilkan Slide 2
        frame_result.pack(pady=20)
        frame_intro.pack_forget()
        frame_input.pack_forget()
        btn_hitung.pack_forget()
    elif slide_number == 3:
        # Menampilkan Slide 3 (Grafik)
        btn_show_graph.pack_forget()
        frame_result.pack_forget()
        show_graph()

# Fungsi untuk menampilkan grafik
def show_graph():
    global canvas  # Menyimpan canvas sebagai variabel global
    risiko_value = slider_risiko.get()
    pengembalian_value = slider_pengembalian.get()
    jangka_waktu_value = slider_jangka_waktu.get()

    # Membuat grafik
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Grafik untuk Risiko
    x_risiko = range(0, 61)
    y_rendah_risiko = [max(0, min(1, (30 - i) / 30)) for i in x_risiko]
    y_sedang_risiko = [max(0, min((i - 10) / 20, (50 - i) / 20)) for i in x_risiko]
    y_tinggi_risiko = [max(0, min((i - 40) / 10, 1)) for i in x_risiko]
    axs[0].plot(x_risiko, y_rendah_risiko, label="Rendah", color="blue")
    axs[0].plot(x_risiko, y_sedang_risiko, label="Sedang", color="green")
    axs[0].plot(x_risiko, y_tinggi_risiko, label="Tinggi", color="red")
    axs[0].axvline(x=risiko_value, color='black', linestyle='--', label=f'Value: {risiko_value}')
    axs[0].set_title("Fungsi Keanggotaan Risiko")
    axs[0].set_xlabel("Tingkat Risiko")
    axs[0].set_ylabel("Keanggotaan")
    axs[0].legend()

    # Grafik untuk Pengembalian
    x_pengembalian = range(0, 51)
    y_rendah_pengembalian = [max(0, min(1, (20 - i) / 20)) for i in x_pengembalian]
    y_sedang_pengembalian = [max(0, min((i - 5) / 15, (35 - i) / 15)) for i in x_pengembalian]
    y_tinggi_pengembalian = [max(0, min((i - 30) / 10, 1)) for i in x_pengembalian]
    axs[1].plot(x_pengembalian, y_rendah_pengembalian, label="Rendah", color="blue")
    axs[1].plot(x_pengembalian, y_sedang_pengembalian, label="Sedang", color="green")
    axs[1].plot(x_pengembalian, y_tinggi_pengembalian, label="Tinggi", color="red")
    axs[1].axvline(x=pengembalian_value, color='black', linestyle='--', label=f'Value: {pengembalian_value}')
    axs[1].set_title("Fungsi Keanggotaan Pengembalian")
    axs[1].set_xlabel("Potensi Pengembalian")
    axs[1].set_ylabel("Keanggotaan")
    axs[1].legend()

    # Grafik untuk Jangka Waktu
    x_jangka_waktu = [i / 10 for i in range(0, 31)]  # Jangka waktu dari 0 sampai 3 tahun
    y_pendek = [max(0, min(1, (1 - i) / 1)) for i in x_jangka_waktu]
    y_sedang = [max(0, min((i - 0.5) / 0.5, (2 - i) / 0.5)) for i in x_jangka_waktu]
    y_panjang = [max(0, min((i - 1.5) / 0.5, 1)) for i in x_jangka_waktu]
    axs[2].plot(x_jangka_waktu, y_pendek, label="Pendek", color="blue")
    axs[2].plot(x_jangka_waktu, y_sedang, label="Sedang", color="green")
    axs[2].plot(x_jangka_waktu, y_panjang, label="Panjang", color="red")
    axs[2].axvline(x=jangka_waktu_value, color='black', linestyle='--', label=f'Value: {jangka_waktu_value} tahun')
    axs[2].set_title("Fungsi Keanggotaan Jangka Waktu")
    axs[2].set_xlabel("Jangka Waktu (tahun)")
    axs[2].set_ylabel("Keanggotaan")
    axs[2].legend()

    # Menampilkan grafik pada Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Membuat aplikasi GUI
root = tk.Tk()
root.title("Rekomendasi Investasi Cryptocurrency")
root.geometry("900x600")

# Frame untuk halaman awal (Slide 0)
frame_intro = tk.Frame(root, bg="#e3f2fd")
frame_intro.pack()

label_welcome = tk.Label(frame_intro, text="Selamat Datang di Aplikasi Rekomendasi Investasi Cryptocurrency", 
                         font=("Helvetica", 18, "bold"), bg="#e3f2fd", fg="#333")
label_welcome.pack(pady=20)

label_description = tk.Label(frame_intro, text="Optimalkan investasi Anda dengan kriteria yang tepat.",
                              font=("Helvetica", 14), bg="#e3f2fd", fg="#555", wraplength=600, justify="center")
label_description.pack(pady=10)

btn_start = tk.Button(frame_intro, text="Mulai", font=("Helvetica", 16, "bold"), 
                       bg="#1a73e8", fg="white", command=lambda: show_slide(1))
btn_start.pack(pady=20)

# Frame untuk input (Slide 1)
frame_input = tk.Frame(root, bg="#f4f4f9")

# Slider untuk tingkat risiko
label_risiko = tk.Label(frame_input, text="Tingkat Risiko (0-50):", font=("Helvetica", 12), bg="#f4f4f9", fg="#333")
label_risiko.grid(row=0, column=0, padx=10, pady=10, sticky="w")
slider_risiko = tk.Scale(frame_input, from_=0, to=50, orient="horizontal", length=300, font=("Helvetica", 12))
slider_risiko.grid(row=0, column=1, padx=10, pady=10)

# Slider untuk potensi pengembalian
label_pengembalian = tk.Label(frame_input, text="Potensi Pengembalian (0-50):", font=("Helvetica", 12), bg="#f4f4f9", fg="#333")
label_pengembalian.grid(row=1, column=0,
                                padx=10, pady=10, sticky="w")
slider_pengembalian = tk.Scale(frame_input, from_=0, to=50, orient="horizontal", length=300, font=("Helvetica", 12))
slider_pengembalian.grid(row=1, column=1, padx=10, pady=10)

# Slider untuk jangka waktu
label_jangka_waktu = tk.Label(frame_input, text="Jangka Waktu (tahun):", font=("Helvetica", 12), bg="#f4f4f9", fg="#333")
label_jangka_waktu.grid(row=2, column=0, padx=10, pady=10, sticky="w")
slider_jangka_waktu = tk.Scale(frame_input, from_=0, to=3, orient="horizontal", length=300, font=("Helvetica", 12), resolution=0.1)
slider_jangka_waktu.grid(row=2, column=1, padx=10, pady=10)

# Tombol hitung
btn_hitung = tk.Button(root, text="Hitung Rekomendasi", font=("Helvetica", 14, "bold"), bg="#1a73e8", fg="white", command=hitung_rekomendasi)

# Frame untuk hasil (Slide 2)
frame_result = tk.Frame(root, bg="#f4f4f9")
result_risiko = tk.Label(frame_result, text="", font=("Helvetica", 12), bg="#f4f4f9", fg="#333")
result_risiko.pack()
result_pengembalian = tk.Label(frame_result, text="", font=("Helvetica", 12), bg="#f4f4f9", fg="#333")
result_pengembalian.pack()
result_jangka_waktu = tk.Label(frame_result, text="", font=("Helvetica", 12), bg="#f4f4f9", fg="#333")
result_jangka_waktu.pack()
result_output = tk.Label(frame_result, text="", font=("Helvetica", 14, "bold"), bg="#f4f4f9", fg="#1a73e8")
result_output.pack()

# Tombol untuk grafik
btn_show_graph = tk.Button(root, text="Tampilkan Grafik", font=("Helvetica", 14), bg="#34a853", fg="white", command=lambda: show_slide(3))
btn_back = tk.Button(root, text="Kembali", font=("Helvetica", 14), bg="#fbbc04", fg="white", command=lambda: show_slide(0))

# Menampilkan Slide 0
show_slide(0)
root.mainloop()