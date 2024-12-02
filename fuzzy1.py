import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

#define semesta fuzzy
popularitas = ctrl.Antecedent(np.arange(0, 10, 1), 'popularitas') #ini ganti apa aja bisa soalnya ini kaya kriteria buat fuzzy gitu (itu di np. arrange ada yang (0, 11, 1 itu artinya dari 0 sampe 10, 1 itu jaraknya))
stabilitas = ctrl.Antecedent(np.arange(0, 10, 1), 'stabilitas') #ini hampir sama kaya atas itu loh
potensi_keuntungan = ctrl.Antecedent(np.arange(0, 11, 1), 'potensi_keuntungan') #ini juga sama kaya atas itu loh
keputusan_investasi = ctrl.Consequent(np.arange(0, 10, 1), 'keputusan_investasi') #ini juga sama kaya atas itu loh ini kayanya buat definisi variable hasil dari hitung hitungannya

# Define fuzzy membership functions
popularitas['rendah'] = fuzz.trimf(popularitas.universe, [0, 1.5, 3])  #ini membership functionnya si popularitas, trimf itu membership functionnya itu triangle, popularitas.universe itu semesta dari popularitas, [0, 0, 5] itu nilai dari membership functionnya
popularitas['sedang'] = fuzz.trimf(popularitas.universe, [4, 5.5, 6]) 
popularitas['tinggi'] = fuzz.trimf(popularitas.universe, [7, 8.5, 10]) 

#membership functionnya si stabilitas
stabilitas['tidak'] = fuzz.trimf(stabilitas.universe, [0, 1.5, 3]) 
stabilitas['sedang'] = fuzz.trimf(stabilitas.universe, [4, 5.5, 6]) 
stabilitas['sangat'] = fuzz.trimf(stabilitas.universe, [7, 8.5, 10]) 

#membership functionnya si potential gain
potensi_keuntungan['dikit'] = fuzz.trimf(potensi_keuntungan.universe, [0, 1.5, 3])  
potensi_keuntungan['sedang'] = fuzz.trimf(potensi_keuntungan.universe, [4, 5.5, 6]) 
potensi_keuntungan['banyak'] = fuzz.trimf(potensi_keuntungan.universe, [7, 8.5, 10]) 

#membership functionnya si investment decision
keputusan_investasi['tidak_rekomen'] = fuzz.trimf(keputusan_investasi.universe, [0, 1.5, 3])  
keputusan_investasi['rekomen'] = fuzz.trimf(keputusan_investasi.universe, [4, 5.5, 6]) 
keputusan_investasi['sangat_rekomen'] = fuzz.trimf(keputusan_investasi.universe, [7, 8.5, 10])    

#rules lek disini ada berapa terserah dah
rule1 = ctrl.Rule(stabilitas['tidak'] & popularitas['tinggi'] & potensi_keuntungan['banyak'], keputusan_investasi['rekomen']) #rule 1 ini kalo stabilitas low, popularitas high, potential gain high maka investment decision highly recommended
rule2 = ctrl.Rule(stabilitas['sedang'] & popularitas['sedang'] & potensi_keuntungan['sedang'], keputusan_investasi['rekomen']) #rule 2 ini kalo stabilitas medium, popularitas medium, potential gain medium maka investment decision recommended
rule3 = ctrl.Rule(stabilitas['sangat'] | popularitas['rendah'] | potensi_keuntungan['dikit'], keputusan_investasi['tidak_rekomen']) #rule 3 ini kalo stabilitas high atau popularitas low atau potential gain low maka investment decision not recommended
rule4 = ctrl.Rule(stabilitas['sangat'] & popularitas['tinggi'] & potensi_keuntungan['banyak'], keputusan_investasi['sangat_rekomen']) #rule 4 ini kalo stabilitas low dan popularitas low dan potential gain low maka investment decision not recommended 

keputusan = ctrl.ControlSystem([rule1, rule2, rule3, rule4]) #ini buat ngegabungin rule rule diatas
hasil_sim = ctrl.ControlSystemSimulation(keputusan) #ini buat ngejalanin rule rule diatas biar bisa dihitung hasilnya 

print(keputusan_investasi)
print(keputusan_investasi.terms)
#GUInya
def hitung():
    vol = float(stabilitas_entry.get())
    pop = float(popularitas_entry.get())
    gain = float(potensi_keuntungan_entry.get())

    # Masukkan input
    hasil_sim.input['popularitas'] = pop
    hasil_sim.input['stabilitas'] = vol
    hasil_sim.input['potensi_keuntungan'] = gain

    # Debugging setelah compute
    print("Output setelah compute:", hasil_sim.output)

    hasil_keputusan = hasil_sim.output['keputusan_investasi']

    if hasil_keputusan <= 3:
        result.set(f"Hasil: {hasil_keputusan:.2f} (tidak rekomen)")
    elif hasil_keputusan <= 6:
        result.set(f"Hasil: {hasil_keputusan:.2f} (rekomen)")
    else:
        result.set(f"Hasil: {hasil_keputusan:.2f} (sangat amat rekomen)")
    #result.set(f"Hasil: {hasil_sim.output['keputusan_investasi']:.2f}") #ini buat nampilin hasilnya
         

#ini buat windows guinya biar muncul
root = tk.Tk()
root.title("Crypto Investment Fuzzy Logic")

#ini buat inputan popularitas
ttk.Label(root, text="popularitas (0-10):").grid(row=1, column=0, padx=10, pady=10)
popularitas_entry = ttk.Entry(root)
popularitas_entry.grid(row=1, column=1, padx=10, pady=10)

#ini buat inputan stabilitas
ttk.Label(root, text="stabilitas (0-10):").grid(row=0, column=0, padx=10, pady=10)
stabilitas_entry = ttk.Entry(root)
stabilitas_entry.grid(row=0, column=1, padx=10, pady=10)

#ini buat inputan potential gain
ttk.Label(root, text="Potensi keuntungan (0-10):").grid(row=2, column=0, padx=10, pady=10)
potensi_keuntungan_entry = ttk.Entry(root)
potensi_keuntungan_entry.grid(row=2, column=1, padx=10, pady=10)

#ini buat tombol hitung
hitung_button = ttk.Button(root, text="Hitung", command=hitung)
hitung_button.grid(row=3, column=0, columnspan=2, pady=10)

#ini buat nampilin hasilnya
result = tk.StringVar()
result_label = ttk.Label(root, textvariable=result, font=("Helvetica", 14))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop() #ini buat jalanin windows guinya
