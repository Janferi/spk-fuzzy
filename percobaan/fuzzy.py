import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import ttk

# Define input and output variables
volatility = ctrl.Antecedent(np.arange(0, 11, 1), 'volatility')
popularity = ctrl.Antecedent(np.arange(0, 11, 1), 'popularity')
potential_gain = ctrl.Antecedent(np.arange(0, 11, 1), 'potential_gain')
investment_decision = ctrl.Consequent(np.arange(0, 11, 1), 'investment_decision')

# Define fuzzy membership functions
volatility['low'] = fuzz.trimf(volatility.universe, [0, 0, 5])
volatility['medium'] = fuzz.trimf(volatility.universe, [0, 5, 10])
volatility['high'] = fuzz.trimf(volatility.universe, [5, 10, 10])

popularity['low'] = fuzz.trimf(popularity.universe, [0, 0, 5])
popularity['medium'] = fuzz.trimf(popularity.universe, [0, 5, 10])
popularity['high'] = fuzz.trimf(popularity.universe, [5, 10, 10])

potential_gain['low'] = fuzz.trimf(potential_gain.universe, [0, 0, 5])
potential_gain['medium'] = fuzz.trimf(potential_gain.universe, [0, 5, 10])
potential_gain['high'] = fuzz.trimf(potential_gain.universe, [5, 10, 10])

investment_decision['not_recommended'] = fuzz.trimf(investment_decision.universe, [0, 0, 5])
investment_decision['recommended'] = fuzz.trimf(investment_decision.universe, [0, 5, 10])
investment_decision['highly_recommended'] = fuzz.trimf(investment_decision.universe, [5, 10, 10])

# Define fuzzy rules
rule1 = ctrl.Rule(volatility['low'] & popularity['high'] & potential_gain['high'], investment_decision['highly_recommended'])
rule2 = ctrl.Rule(volatility['medium'] & popularity['medium'] & potential_gain['medium'], investment_decision['recommended'])
rule3 = ctrl.Rule(volatility['high'] | popularity['low'] | potential_gain['low'], investment_decision['not_recommended'])

# Control system
investment_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
investment_sim = ctrl.ControlSystemSimulation(investment_ctrl)

# GUI using Tkinter
def calculate_investment():
    vol = float(volatility_entry.get())
    pop = float(popularity_entry.get())
    gain = float(potential_gain_entry.get())

    investment_sim.input['volatility'] = vol
    investment_sim.input['popularity'] = pop
    investment_sim.input['potential_gain'] = gain

    investment_sim.compute()
    result.set(f"Investment Decision Score: {investment_sim.output['investment_decision']:.2f}")

# Create GUI window
root = tk.Tk()
root.title("Crypto Investment Fuzzy Logic")

# Input fields
ttk.Label(root, text="Volatility (0-10):").grid(row=0, column=0, padx=10, pady=10)
volatility_entry = ttk.Entry(root)
volatility_entry.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(root, text="Popularity (0-10):").grid(row=1, column=0, padx=10, pady=10)
popularity_entry = ttk.Entry(root)
popularity_entry.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(root, text="Potential Gain (0-10):").grid(row=2, column=0, padx=10, pady=10)
potential_gain_entry = ttk.Entry(root)
potential_gain_entry.grid(row=2, column=1, padx=10, pady=10)

# Output field
result = tk.StringVar()
result_label = ttk.Label(root, textvariable=result, font=("Helvetica", 14))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Calculate button
calculate_button = ttk.Button(root, text="Calculate", command=calculate_investment)
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
