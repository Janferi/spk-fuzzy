import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import ttk, messagebox

# Define fuzzy universe
popularitas = ctrl.Antecedent(np.arange(0, 10, 1), 'popularitas')
stabilitas = ctrl.Antecedent(np.arange(0, 10, 1), 'stabilitas')
potensi_keuntungan = ctrl.Antecedent(np.arange(0, 11, 1), 'potensi_keuntungan')
keputusan_investasi = ctrl.Consequent(np.arange(0, 10, 1), 'keputusan_investasi')

# Define fuzzy membership functions
popularitas['rendah'] = fuzz.trimf(popularitas.universe, [0, 1.5, 3])
popularitas['sedang'] = fuzz.trimf(popularitas.universe, [4, 5.5, 6]) 
popularitas['tinggi'] = fuzz.trimf(popularitas.universe, [7, 8.5, 10]) 

stabilitas['tidak'] = fuzz.trimf(stabilitas.universe, [0, 1.5, 3]) 
stabilitas['sedang'] = fuzz.trimf(stabilitas.universe, [4, 5.5, 6]) 
stabilitas['sangat'] = fuzz.trimf(stabilitas.universe, [7, 8.5, 10]) 

potensi_keuntungan['dikit'] = fuzz.trimf(potensi_keuntungan.universe, [0, 1.5, 3])  
potensi_keuntungan['sedang'] = fuzz.trimf(potensi_keuntungan.universe, [4, 5.5, 6]) 
potensi_keuntungan['banyak'] = fuzz.trimf(potensi_keuntungan.universe, [7, 8.5, 10]) 

keputusan_investasi['tidak_rekomen'] = fuzz.trimf(keputusan_investasi.universe, [0, 1.5, 3])  
keputusan_investasi['rekomen'] = fuzz.trimf(keputusan_investasi.universe, [4, 5.5, 6]) 
keputusan_investasi['sangat_rekomen'] = fuzz.trimf(keputusan_investasi.universe, [7, 8.5, 10])    

# Define fuzzy rules
rule1 = ctrl.Rule(stabilitas['tidak'] & popularitas['tinggi'] & potensi_keuntungan['banyak'], keputusan_investasi['rekomen'])
rule2 = ctrl.Rule(stabilitas['sedang'] & popularitas['sedang'] & potensi_keuntungan['sedang'], keputusan_investasi['rekomen'])
rule3 = ctrl.Rule(stabilitas['sangat'] | popularitas['rendah'] | potensi_keuntungan['dikit'], keputusan_investasi['tidak_rekomen'])
rule4 = ctrl.Rule(stabilitas['sangat'] & popularitas['tinggi'] & potensi_keuntungan['banyak'], keputusan_investasi['sangat_rekomen'])

# Create control system
keputusan = ctrl.ControlSystem([rule1, rule2, rule3, rule4])

def hitung():
    try:
        # Create a new simulation for each calculation
        hasil_sim = ctrl.ControlSystemSimulation(keputusan)

        # Get input values
        vol = float(stabilitas_entry.get())
        pop = float(popularitas_entry.get())
        gain = float(potensi_keuntungan_entry.get())

        # Input fuzzy values
        hasil_sim.input['popularitas'] = pop
        hasil_sim.input['stabilitas'] = vol
        hasil_sim.input['potensi_keuntungan'] = gain

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

# Stabilitas Input
ttk.Label(root, text="Stabilitas (0-10):").grid(row=0, column=0, padx=10, pady=10)
stabilitas_entry = ttk.Entry(root)
stabilitas_entry.grid(row=0, column=1, padx=10, pady=10)

# Popularitas Input
ttk.Label(root, text="Popularitas (0-10):").grid(row=1, column=0, padx=10, pady=10)
popularitas_entry = ttk.Entry(root)
popularitas_entry.grid(row=1, column=1, padx=10, pady=10)

# Potensi Keuntungan Input
ttk.Label(root, text="Potensi Keuntungan (0-10):").grid(row=2, column=0, padx=10, pady=10)
potensi_keuntungan_entry = ttk.Entry(root)
potensi_keuntungan_entry.grid(row=2, column=1, padx=10, pady=10)

# Hitung Button
hitung_button = ttk.Button(root, text="Hitung", command=hitung)
hitung_button.grid(row=3, column=0, columnspan=2, pady=10)

# Result Display
result = tk.StringVar()
result_label = ttk.Label(root, textvariable=result, font=("Helvetica", 14))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()