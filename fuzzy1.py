import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

#define semesta fuzzy
popularitas = ctrl.Antecedent(np.arange(0, 11, 1), 'popularitas') #ini ganti apa aja bisa soalnya ini kaya kriteria buat fuzzy gitu (itu di np. arrange ada yang (0, 11, 1 itu artinya dari 0 sampe 10, 1 itu jaraknya))
stabilitas = ctrl.Antecedent(np.arange(0, 11, 1), 'stabilitas') #ini hampir sama kaya atas itu loh
potensi_keuntungan = ctrl.Antecedent(np.arange(0, 11, 1), 'potensi_keuntungan') #ini juga sama kaya atas itu loh
keputusan_investasi = ctrl.Consequent(np.arange(0, 11, 1), 'keputusan_investasi') #ini juga sama kaya atas itu loh ini kayanya buat definisi variable hasil dari hitung hitungannya

# Define fuzzy membership functions
popularitas['low'] = fuzz.trimf(popularitas.universe, [0, 0, 5]) #ini membership functionnya si popularitas, trimf itu membership functionnya itu triangle, popularitas.universe itu semesta dari popularitas, [0, 0, 5] itu nilai dari membership functionnya
popularitas['medium'] = fuzz.trimf(popularitas.universe, [0, 5, 10]) 
popularitas['high'] = fuzz.trimf(popularitas.universe, [5, 10, 10]) 


#membership functionnya si stabilitas
stabilitas['low'] = fuzz.trimf(stabilitas.universe, [0, 0, 5]) 
stabilitas['medium'] = fuzz.trimf(stabilitas.universe, [0, 5, 10]) 
stabilitas['high'] = fuzz.trimf(stabilitas.universe, [5, 10, 10]) 

potensi_keuntungan['low'] = fuzz.trimf(potensi_keuntungan.universe, [0, 0, 5]) 
potensi_keuntungan['medium'] = fuzz.trimf(potensi_keuntungan.universe, [0, 5, 10]) 
potensi_keuntungan['high'] = fuzz.trimf(potensi_keuntungan.universe, [5, 10, 10]) 

keputusan_investasi['not_recommended'] = fuzz.trimf(keputusan_investasi.universe, [0, 0, 5]) 
keputusan_investasi['recommended'] = fuzz.trimf(keputusan_investasi.universe, [0, 5, 10]) 
keputusan_investasi['highly_recommended'] = fuzz.trimf(keputusan_investasi.universe, [5, 10, 10]) 

#rules lek disini ada berapa terserah dah
rule1 = ctrl.Rule(stabilitas['low'] & popularitas['high'] & potensi_keuntungan['high'], keputusan_investasi['highly_recommended']) #rule 1 ini kalo stabilitas low, popularitas high, potential gain high maka investment decision highly recommended
rule2 = ctrl.Rule(stabilitas['medium'] & popularitas['medium'] & potensi_keuntungan['medium'], keputusan_investasi['recommended']) #rule 2 ini kalo stabilitas medium, popularitas medium, potential gain medium maka investment decision recommended
rule3 = ctrl.Rule(stabilitas['high'] | popularitas['low'] | potensi_keuntungan['low'], keputusan_investasi['not_recommended']) #rule 3 ini kalo stabilitas high atau popularitas low atau potential gain low maka investment decision not recommended
rule4 = ctrl.Rule(stabilitas['low'] & popularitas['low'] & potensi_keuntungan['low'], keputusan_investasi['not_recommended']) #rule 4 ini kalo stabilitas low dan popularitas low dan potential gain low maka investment decision not recommended 

keputusan = ctrl.ControlSystem([rule1, rule2, rule3, rule4]) #ini buat ngegabungin rule rule diatas
hasil_sim = ctrl.ControlSystemSimulation(keputusan) #ini buat ngejalanin rule rule diatas biar bisa dihitung hasilnya 

#GUInya
def hitung():
    vol = float(stabilitas_entry.get()) #ini buat ngambil nilai dari inputan stabilitas
    pop = float(popularitas_entry.get()) #ini buat ngambil nilai dari inputan popularitas
    gain = float(potensi_keuntungan_entry.get()) #ini buat ngambil nilai dari inputan potential gain

    hasil_sim.input['popularitas'] = pop #ini buat ngasih nilai inputan ke popularitas
    hasil_sim.input['stabilitas'] = vol #ini buat ngasih nilai inputan ke stabilitas
    hasil_sim.input['potensi_keuntungan'] = gain #ini buat ngasih nilai inputan ke potential gain

    hasil_sim.compute() #ini buat ngitung hasilnya
    keputusan_investasi = hasil_sim.output['keputusan_investasi'] #ini buat ngambil hasilnya

    if keputusan_investasi >= 5:
        result.set(f"Hasil: {hasil_sim.output['keputusan_investasi']:.2f} (Not Recommended)")
    elif keputusan_investasi < 8:
        result.set(f"Hasil: {hasil_sim.output['keputusan_investasi']:.2f} (Recommended)")
    else:
        result.set(f"Hasil: {hasil_sim.output['keputusan_investasi']:.2f} (Highly Recommended)")
    
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
