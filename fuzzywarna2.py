import tkinter as tk
from tkinter import ttk


# Fungsi untuk menghitung rekomendasi dan menampilkan grafik
def hitung_rekomendasi():
    try:
        # Mengambil nilai dari slider
        aktor_value = slider_aktor.get()
        lokasi_value = slider_lokasi.get()

        # Fungsi keanggotaan untuk biaya aktor
        def fuzzy_membership_aktor(value):
            """Hitung derajat keanggotaan untuk Biaya Aktor."""
            rendah = max(0, min(1, (400 - value) / 400))  # Nilai maks 400
            sedang = max(0, min((value - 200) / 200, (600 - value) / 200))  # Nilai 200-600
            tinggi = max(0, min((value - 500) / 200, 1))  # Nilai min 500
            return {"rendah": rendah, "sedang": sedang, "tinggi": tinggi}

        # Fungsi keanggotaan untuk biaya lokasi
        def fuzzy_membership_lokasi(value):
            """Hitung derajat keanggotaan untuk Biaya Lokasi."""
            rendah = max(0, min(1, (400 - value) / 400))  # Nilai maks 400
            sedang = max(0, min((value - 200) / 200, (600 - value) / 200))  # Nilai 200-600
            tinggi = max(0, min((value - 500) / 200, 1))  # Nilai min 500
            return {"rendah": rendah, "sedang": sedang, "tinggi": tinggi}

        # Keanggotaan biaya aktor dan lokasi
        aktor_membership = fuzzy_membership_aktor(aktor_value)
        lokasi_membership = fuzzy_membership_lokasi(lokasi_value)

        # Aturan fuzzy
        rules = [
            {"aktor": "rendah", "lokasi": "rendah", "output": "Minimal", "reason": "Aktor dan lokasi memiliki biaya rendah."},
            {"aktor": "rendah", "lokasi": "sedang", "output": "Minimal", "reason": "Aktor memiliki biaya rendah, lokasi sedang."},
            {"aktor": "rendah", "lokasi": "tinggi", "output": "Optimal", "reason": "Aktor biaya rendah, lokasi biaya tinggi."},
            {"aktor": "sedang", "lokasi": "rendah", "output": "Minimal", "reason": "Aktor biaya sedang, lokasi biaya rendah."},
            {"aktor": "sedang", "lokasi": "sedang", "output": "Optimal", "reason": "Aktor dan lokasi memiliki biaya sedang."},
            {"aktor": "sedang", "lokasi": "tinggi", "output": "Maksimal", "reason": "Aktor biaya sedang, lokasi biaya tinggi."},
            {"aktor": "tinggi", "lokasi": "rendah", "output": "Optimal", "reason": "Aktor biaya tinggi, lokasi biaya rendah."},
            {"aktor": "tinggi", "lokasi": "sedang", "output": "Maksimal", "reason": "Aktor biaya tinggi, lokasi biaya sedang."},
            {"aktor": "tinggi", "lokasi": "tinggi", "output": "Maksimal", "reason": "Aktor dan lokasi memiliki biaya tinggi."},
        ]

        # Cari aturan dengan keanggotaan tertinggi
        best_rule = None
        best_similarity = 0  # Tingkat keanggotaan tertinggi
        
        for rule in rules:
            aktor_degree = aktor_membership[rule["aktor"]]
            lokasi_degree = lokasi_membership[rule["lokasi"]]
            similarity = min(aktor_degree, lokasi_degree)  # Derajat similaritas
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_rule = rule
        
        # Output kategori berdasarkan aturan terbaik
        if best_rule:
            output = best_rule["output"]
            reason = best_rule["reason"]
        else:
            output = "Tidak ada hasil"
            reason = "Tidak ada aturan yang sesuai."

        # Menampilkan hasil di label
        result_aktor.config(text=f"Biaya Aktor (dalam Juta): {aktor_value}")
        result_lokasi.config(text=f"Biaya Lokasi (dalam Juta): {lokasi_value}")
        result_output.config(text=f"Total anggaran yang dikeluarkan: {output}")
        result_reason.config(text=f"Alasan: {reason}")

        # Menampilkan tombol grafik setelah perhitungan selesai
        btn_show_graph.pack(pady=10)
        btn_back.pack(pady=10)

        # Pindah ke Slide 2 untuk menampilkan hasil
        show_slide(2)
    
    except ValueError:
        # Jika input tidak valid, tampilkan pesan error
        result_aktor.config(text="Masukkan nilai yang valid!")
        result_lokasi.config(text="Masukkan nilai yang valid!")
        result_output.config(text="Masukkan nilai yang valid!")

# Fungsi untuk menampilkan slide tertentu
def show_slide(slide_number):
    if slide_number == 0:
        # Menampilkan Slide 0 (Halaman Pertama)
        frame_start.pack(pady=50)
        frame_input.pack_forget()
        frame_result.pack_forget()
        if 'canvas' in globals():
            canvas.get_tk_widget().pack_forget()  # Menghapus grafik jika ada
        btn_show_graph.pack_forget()
        btn_back.pack_forget()
    elif slide_number == 1:
        # Menampilkan Slide 1
        frame_start.pack_forget()
        frame_input.pack(pady=20)
        btn_hitung.pack(pady=20)
        frame_result.pack_forget()
        if 'canvas' in globals():
            canvas.get_tk_widget().pack_forget()
        btn_show_graph.pack_forget()
        btn_back.pack_forget()
    elif slide_number == 2:
        # Menampilkan Slide 2
        frame_start.pack_forget()
        frame_result.pack(pady=20)
        frame_input.pack_forget()
        btn_hitung.pack_forget()
    elif slide_number == 3:
        # Menampilkan Slide 3 (Grafik)
        btn_show_graph.pack_forget()
        frame_result.pack_forget()
        if 'canvas' in globals():
            canvas.get_tk_widget().pack_forget()
        show_graph()


# Fungsi untuk menampilkan slide tertentu
def show_slide(slide_number):
    if slide_number == 0:
        # Menampilkan Slide 0
        frame_intro.pack(pady=20)
        frame_input.pack_forget()  # Menyembunyikan Slide 1
        frame_result.pack_forget()  # Menyembunyikan Slide 2
        if 'canvas' in globals():
            canvas.get_tk_widget().pack_forget()  # Menghapus grafik jika ada
        btn_show_graph.pack_forget()  # Menyembunyikan tombol grafik
        btn_back.pack_forget()  # Menyembunyikan tombol kembali
    elif slide_number == 1:
        # Menampilkan Slide 1
        frame_intro.pack_forget()  # Menyembunyikan Slide 0
        frame_input.pack(pady=20)
        btn_hitung.pack(pady=20)  # Pastikan tombol ada di bawah input
        frame_result.pack_forget()  # Menyembunyikan Slide 2
        if 'canvas' in globals():
            canvas.get_tk_widget().pack_forget()  # Menghapus grafik jika ada
        btn_show_graph.pack_forget()  # Menyembunyikan tombol grafik
        btn_back.pack_forget()  # Menyembunyikan tombol kembali
    elif slide_number == 2:
        # Menampilkan Slide 2
        frame_result.pack(pady=20)
        frame_intro.pack_forget()  # Menyembunyikan Slide 0
        frame_input.pack_forget()  # Menyembunyikan Slide 1
        btn_hitung.pack_forget()  # Menyembunyikan tombol hitung
    elif slide_number == 3:
        # Menampilkan Slide 3 (Grafik)
        btn_show_graph.pack_forget()  # Menyembunyikan tombol hitung
        frame_result.pack_forget()  # Menyembunyikan Slide 2
        if 'canvas' in globals():
            canvas.get_tk_widget().pack_forget()  # Menghapus grafik sebelumnya
        show_graph()
# Fungsi untuk menampilkan grafik
def show_graph():
    global canvas  # Menyimpan canvas sebagai variabel global
    aktor_value = slider_aktor.get()
    lokasi_value = slider_lokasi.get()

    # Membuat grafik
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    # Grafik untuk Biaya Aktor
    x_aktor = range(0, 700)
    y_rendah_aktor = [max(0, min(1, (400 - i) / 400)) for i in x_aktor]
    y_sedang_aktor = [max(0, min((i - 200) / 200, (600 - i) / 200)) for i in x_aktor]
    y_tinggi_aktor = [max(0, min((i - 500) / 200, 1)) for i in x_aktor]
    axs[0].plot(x_aktor, y_rendah_aktor, label="Rendah", color="blue")
    axs[0].plot(x_aktor, y_sedang_aktor, label="Sedang", color="green")
    axs[0].plot(x_aktor, y_tinggi_aktor, label="Tinggi", color="red")
    axs[0].axvline(x=aktor_value, color='black', linestyle='--', label=f'Value: {aktor_value}')
    axs[0].set_title("Fungsi Keanggotaan Biaya Aktor")
    axs[0].set_xlabel("Biaya Aktor (juta)")
    axs[0].set_ylabel("Keanggotaan")
    axs[0].legend()

    # Grafik untuk Biaya Lokasi
    x_lokasi = range(0, 700)
    y_rendah_lokasi = [max(0, min(1, (400 - i) / 400)) for i in x_lokasi]
    y_sedang_lokasi = [max(0, min((i - 200) / 200, (600 - i) / 200)) for i in x_lokasi]
    y_tinggi_lokasi = [max(0, min((i - 500) / 200, 1)) for i in x_lokasi]
    axs[1].plot(x_lokasi, y_rendah_lokasi, label="Rendah", color="blue")
    axs[1].plot(x_lokasi, y_sedang_lokasi, label="Sedang", color="green")
    axs[1].plot(x_lokasi, y_tinggi_lokasi, label="Tinggi", color="red")
    axs[1].axvline(x=lokasi_value, color='black', linestyle='--', label=f'Value: {lokasi_value}')
    axs[1].set_title("Fungsi Keanggotaan Biaya Lokasi")
    axs[1].set_xlabel("Biaya Lokasi (juta)")
    axs[1].set_ylabel("Keanggotaan")
    axs[1].legend()

    # Menampilkan grafik pada Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
# Membuat aplikasi GUI
root = tk.Tk()
root.title("Rekomendasi Biaya Aktor dan Lokasi")
root.geometry("800x600")

# Frame untuk halaman awal (Slide 0)
frame_intro = tk.Frame(root, bg="#e3f2fd")
frame_intro.pack()

label_welcome = tk.Label(frame_intro, text="Selamat Datang di Aplikasi Rekomendasi Biaya Aktor dan Lokasi", 
                         font=("Helvetica", 18, "bold"), bg="#e3f2fd", fg="#333")
label_welcome.pack(pady=20)

label_description = tk.Label(frame_intro, text="Optimalkan anggaran produksi film Anda dengan mudah.",
                              font=("Helvetica", 14), bg="#e3f2fd", fg="#555", wraplength=600, justify="center")
label_description.pack(pady=10)

btn_start = tk.Button(frame_intro, text="Mulai", font=("Helvetica", 16, "bold"), 
                       bg="#1a73e8", fg="white", command=lambda: show_slide(1))
btn_start.pack(pady=20)

# Frame untuk input (Slide 1)
frame_input = tk.Frame(root, bg="#f4f4f9")

# Slider untuk biaya aktor
label_aktor = tk.Label(frame_input, text="Biaya Aktor (Dalam Juta):", font=("Helvetica", 12), bg="#f4f4f9", fg="#333")
label_aktor.grid(row=0, column=0, padx=10, pady=10, sticky="w")
slider_aktor = tk.Scale(frame_input, from_=0, to=700, orient="horizontal", length=300, font=("Helvetica", 12))
slider_aktor.grid(row=0, column=1, padx=10, pady=10)

# Slider untuk biaya lokasi
label_lokasi = tk.Label(frame_input, text="Biaya Lokasi (Dalam Juta):", font=("Helvetica", 12), bg="#f4f4f9", fg="#333")
label_lokasi.grid(row=1, column=0, padx=10, pady=10, sticky="w")
slider_lokasi = tk.Scale(frame_input, from_=0, to=700, orient="horizontal", length=300, font=("Helvetica", 12))
slider_lokasi.grid(row=1, column=1, padx=10, pady=10)

# Tombol hitung
btn_hitung = tk.Button(root, text="Hitung Rekomendasi", font=("Helvetica", 14, "bold"), bg="#1a73e8", fg="white", command=hitung_rekomendasi)

# Frame untuk hasil (Slide 2)
frame_result = tk.Frame(root, bg="#f4f4f9")
result_aktor = tk.Label(frame_result, text="", font=("Helvetica", 12), bg="#f4f4f9", fg="#333")
result_aktor.pack()
result_lokasi = tk.Label(frame_result, text="", font=("Helvetica", 12), bg="#f4f4f9", fg="#333")
result_lokasi.pack()
result_output = tk.Label(frame_result, text="", font=("Helvetica", 14, "bold"), bg="#f4f4f9", fg="#1a73e8")
result_output.pack()
result_reason = tk.Label(frame_result, text="", font=("Helvetica", 12), bg="#f4f4f9", fg="#333", wraplength=600, justify="center")
result_reason.pack()

# Tombol untuk grafik
btn_show_graph = tk.Button(root, text="Tampilkan Grafik", font=("Helvetica", 14), bg="#34a853", fg="white", command=lambda: show_slide(3))
btn_back = tk.Button(root, text="Kembali", font=("Helvetica", 14), bg="#fbbc04", fg="white", command=lambda: show_slide(0))

# Menampilkan Slide 0
show_slide(0)
root.mainloop()