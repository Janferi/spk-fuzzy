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

        # Keanggotaan risiko dan pengembalian
        risiko_membership = fuzzy_membership_risiko(risiko_value)
        pengembalian_membership = fuzzy_membership_pengembalian(pengembalian_value)

        # Semua kombinasi aturan
        rules = [
            {"risiko": "rendah", "pengembalian": "tinggi", "output": "Sangat Direkomendasikan"},
            {"risiko": "rendah", "pengembalian": "sedang", "output": "Direkomendasikan"},
            {"risiko": "sedang", "pengembalian": "tinggi", "output": "Direkomendasikan"},
            {"risiko": "sedang", "pengembalian": "sedang", "output": "Perlu Pertimbangan"},
            {"risiko": "tinggi", "pengembalian": "rendah", "output": "Tidak Direkomendasikan"},
            {"risiko": "tinggi", "pengembalian": "sedang", "output": "Perlu Pertimbangan"},
        ]

        # Mencari aturan terbaik
        best_rule = None
        best_similarity = 0
        
        for rule in rules:
            risiko_degree = risiko_membership[rule["risiko"]]
            pengembalian_degree = pengembalian_membership[rule["pengembalian"]]
            similarity = min(risiko_degree, pengembalian_degree)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_rule = rule
        
        # Keputusan akhir
        output = best_rule["output"] if best_rule else "Tidak Direkomendasikan"

        # Menampilkan hasil di label
        result_risiko.config(text=f"Tingkat Risiko: {risiko_value}")
        result_pengembalian.config(text=f"Potensi Pengembalian: {pengembalian_value}")
        result_output.config(text=f"Rekomendasi: {output}")

        # Menampilkan tombol grafik setelah perhitungan selesai
        btn_show_graph.pack(pady=20)
        btn_back.pack(pady=20)

        # Pindah ke Slide 2 untuk menampilkan hasil
        show_slide(2)
    
    except ValueError:
        # Jika input tidak valid
        result_output.config(text="Input tidak valid!")

# Fungsi untuk menampilkan grafik
def show_graph():
    global canvas  # Menyimpan canvas sebagai variabel global agar dapat dihapus
    if 'canvas' in globals():
        canvas.get_tk_widget().destroy()  # Hapus grafik sebelumnya jika ada

    risiko_value = slider_risiko.get()
    pengembalian_value = slider_pengembalian.get()

    # Membuat grafik
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # Grafik untuk Risiko
    x_risiko = range(1, 11)
    y_rendah_risiko = [max(0, min(1, (5 - i) / 4)) for i in x_risiko]
    y_sedang_risiko = [max(0, min((i - 3) / 2, (7 - i) / 2)) for i in x_risiko]
    y_tinggi_risiko = [max(0, min((i - 6) / 4, 1)) for i in x_risiko]
    axs[0].plot(x_risiko, y_rendah_risiko, label="Rendah", color="blue")
    axs[0].plot(x_risiko, y_sedang_risiko, label="Sedang", color="green")
    axs[0].plot(x_risiko, y_tinggi_risiko, label="Tinggi", color="red")
    axs[0].axvline(x=risiko_value, color='black', linestyle='--', label=f'Value: {risiko_value}')
    axs[0].set_title("Fungsi Keanggotaan Risiko")
    axs[0].set_xlabel("Tingkat Risiko")
    axs[0].set_ylabel("Keanggotaan")
    axs[0].legend()

    # Grafik untuk Pengembalian
    x_pengembalian = range(1, 11)
    y_rendah_pengembalian = [max(0, min(1, (5 - i) / 4)) for i in x_pengembalian]
    y_sedang_pengembalian = [max(0, min((i - 3) / 2, (7 - i) / 2)) for i in x_pengembalian]
    y_tinggi_pengembalian = [max(0, min((i - 6) / 4, 1)) for i in x_pengembalian]
    axs[1].plot(x_pengembalian, y_rendah_pengembalian, label="Rendah", color="blue")
    axs[1].plot(x_pengembalian, y_sedang_pengembalian, label="Sedang", color="green")
    axs[1].plot(x_pengembalian, y_tinggi_pengembalian, label="Tinggi", color="red")
    axs[1].axvline(x=pengembalian_value, color='black', linestyle='--', label=f'Value: {pengembalian_value}')
    axs[1].set_title("Fungsi Keanggotaan Pengembalian")
    axs[1].set_xlabel("Potensi Pengembalian")
    axs[1].set_ylabel("Keanggotaan")
    axs[1].legend()

    # Menampilkan grafik pada Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame_result)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)


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
root.geometry("1000x700")
root.configure(bg="#f0f8ff")

# Komponen GUI
frame_intro = tk.Frame(root, bg="#e3f2fd")
frame_intro.pack()
label_welcome = tk.Label(frame_intro, text="Rekomendasi Investasi Cryptocurrency", font=("Helvetica", 18, "bold"), bg="#e3f2fd")
label_welcome.pack(pady=20)
btn_start = tk.Button(frame_intro, text="Mulai", command=lambda: show_slide(1), bg="#1e88e5", fg="white", font=("Helvetica", 14))
btn_start.pack(pady=20)

frame_input = tk.Frame(root, bg="#f4f4f9")
slider_risiko = tk.Scale(frame_input, from_=1, to=10, orient="horizontal", label="Tingkat Risiko", bg="#f4f4f9", font=("Helvetica", 12))
slider_pengembalian = tk.Scale(frame_input, from_=1, to=10, orient="horizontal", label="Potensi Pengembalian", bg="#f4f4f9", font=("Helvetica", 12))
slider_risiko.pack(pady=20)
slider_pengembalian.pack(pady=20)
btn_calculate = tk.Button(frame_input, text="Hitung Rekomendasi", command=hitung_rekomendasi, bg="#66bb6a", fg="white", font=("Helvetica", 14))
btn_calculate.pack(pady=20)

frame_result = tk.Frame(root, bg="#f4f4f9")
result_risiko = tk.Label(frame_result, text="Tingkat Risiko: ", font=("Helvetica", 14), bg="#f4f4f9")
result_pengembalian = tk.Label(frame_result, text="Potensi Pengembalian: ", font=("Helvetica", 14), bg="#f4f4f9")
result_output = tk.Label(frame_result, text="Rekomendasi: ", font=("Helvetica", 14), bg="#f4f4f9")
result_risiko.pack(pady=10)
result_pengembalian.pack(pady=10)
result_output.pack(pady=10)

btn_show_graph = tk.Button(frame_result, text="Lihat Grafik", command=show_graph, bg="#f57c00", fg="white", font=("Helvetica", 14))
btn_back = tk.Button(frame_result, text="Kembali", command=lambda: show_slide(0), bg="#0288d1", fg="white", font=("Helvetica", 14))

# Mulai aplikasi pada slide 0 (Intro)
show_slide(0)

# Menjalankan aplikasi GUI
root.mainloop()
