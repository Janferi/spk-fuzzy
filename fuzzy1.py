import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import ttk, messagebox

# Define fuzzy universe
tingkat_resiko = ctrl.Antecedent(np.arange(0, 10, 1), 'tingkat_resiko')
jangka_waktu = ctrl.Antecedent(np.arange(0, 10, 1), 'jangka_waktu')
potensi_pengembalian = ctrl.Antecedent(np.arange(0, 11, 1), 'potensi_pengembalian')
keputusan_investasi = ctrl.Consequent(np.arange(0, 10, 1), 'keputusan_investasi')

# Define fuzzy membership functions
tingkat_resiko['tinggi'] = fuzz.trimf(tingkat_resiko.universe, [0, 1.5, 3])
tingkat_resiko['sedang'] = fuzz.trimf(tingkat_resiko.universe, [4, 5.5, 6]) 
tingkat_resiko['rendah'] = fuzz.trimf(tingkat_resiko.universe, [7, 8.5, 10]) 

jangka_waktu['panjang'] = fuzz.trimf(jangka_waktu.universe, [0, 1.5, 3]) 
jangka_waktu['sedang'] = fuzz.trimf(jangka_waktu.universe, [4, 5.5, 6]) 
jangka_waktu['pendek'] = fuzz.trimf(jangka_waktu.universe, [7, 8.5, 10]) 

potensi_pengembalian['dikit'] = fuzz.trimf(potensi_pengembalian.universe, [0, 1.5, 3])  
potensi_pengembalian['sedang'] = fuzz.trimf(potensi_pengembalian.universe, [4, 5.5, 6]) 
potensi_pengembalian['banyak'] = fuzz.trimf(potensi_pengembalian.universe, [7, 8.5, 10]) 

keputusan_investasi['tidak_rekomen'] = fuzz.trimf(keputusan_investasi.universe, [0, 1.5, 3])  
keputusan_investasi['rekomen'] = fuzz.trimf(keputusan_investasi.universe, [4, 5.5, 6]) 
keputusan_investasi['sangat_rekomen'] = fuzz.trimf(keputusan_investasi.universe, [7, 8.5, 10])    

# Define fuzzy rules
rule1 = ctrl.Rule(jangka_waktu['panjang'] & tingkat_resiko['rendah'] & potensi_pengembalian['banyak'], keputusan_investasi['rekomen'])
rule2 = ctrl.Rule(jangka_waktu['sedang'] & tingkat_resiko['sedang'] & potensi_pengembalian['sedang'], keputusan_investasi['rekomen'])
rule3 = ctrl.Rule(jangka_waktu['pendek'] | tingkat_resiko['tinggi'] | potensi_pengembalian['dikit'], keputusan_investasi['tidak_rekomen'])
rule4 = ctrl.Rule(jangka_waktu['pendek'] & tingkat_resiko['rendah'] & potensi_pengembalian['banyak'], keputusan_investasi['sangat_rekomen'])

# Create control system
keputusan = ctrl.ControlSystem([rule1, rule2, rule3, rule4])

def hitung():
    try:
        # Create a new simulation for each calculation
        hasil_sim = ctrl.ControlSystemSimulation(keputusan)

        # Get input values
        vol = float(jangka_waktu_entry.get())
        pop = float(tingkat_resiko_entry.get())
        gain = float(potensi_pengembalian_entry.get())

        # Input fuzzy values
        hasil_sim.input['tingkat_resiko'] = pop
        hasil_sim.input['jangka_waktu'] = vol
        hasil_sim.input['potensi_pengembalian'] = gain

        # Compute the fuzzy output
        hasil_sim.compute()

        # Print debug information
        print("Input values:", pop, vol, gain)
        print("Output keys:", list(hasil_sim.output.keys()))
        
        # Get output (use the correct key)
        hasil_keputusan = hasil_sim.output['keputusan_investasi']

        # Set result based on the output
        if hasil_keputusan <= 3:
            result.set(f"Hasil: {hasil_keputusan:.2f} (tidak rekomen)")
        elif hasil_keputusan <= 6:
            result.set(f"Hasil: {hasil_keputusan:.2f} (rekomen)")
        else:
            result.set(f"Hasil: {hasil_keputusan:.2f} (sangat amat rekomen)")

    except Exception as e:
        # Catch and display any errors
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Crypto Investment Fuzzy Logic")

# jangka_waktu Input
ttk.Label(root, text="jangka_waktu (0-10):").grid(row=0, column=0, padx=10, pady=10)
jangka_waktu_entry = ttk.Entry(root)
jangka_waktu_entry.grid(row=0, column=1, padx=10, pady=10)

# tingkat_resiko Input
ttk.Label(root, text="tingkat_resiko (0-10):").grid(row=1, column=0, padx=10, pady=10)
tingkat_resiko_entry = ttk.Entry(root)
tingkat_resiko_entry.grid(row=1, column=1, padx=10, pady=10)

# Potensi Keuntungan Input
ttk.Label(root, text="Potensi Keuntungan (0-10):").grid(row=2, column=0, padx=10, pady=10)
potensi_pengembalian_entry = ttk.Entry(root)
potensi_pengembalian_entry.grid(row=2, column=1, padx=10, pady=10)

# Hitung Button
hitung_button = ttk.Button(root, text="Hitung", command=hitung)
hitung_button.grid(row=3, column=0, columnspan=2, pady=10)

# Result Display
result = tk.StringVar()
result_label = ttk.Label(root, textvariable=result, font=("Helvetica", 14))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()