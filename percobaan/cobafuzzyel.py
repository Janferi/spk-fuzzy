import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Fungsi keanggotaan fuzzy
def fuzzy_risk(value):
    low = max(0, min(1, (5 - value) / 5))
    medium = max(0, min((value - 3) / 2, (7 - value) / 2))
    high = max(0, min((value - 5) / 5, 1))
    return {"low": low, "medium": medium, "high": high}

def fuzzy_return(value):
    low = max(0, min(1, (5 - value) / 5))
    medium = max(0, min((value - 3) / 2, (7 - value) / 2))
    high = max(0, min((value - 5) / 5, 1))
    return {"low": low, "medium": medium, "high": high}

def fuzzy_time(value):
    short = max(0, min(1, (5 - value) / 5))
    medium = max(0, min((value - 3) / 2, (7 - value) / 2))
    long = max(0, min((value - 5) / 5, 1))
    return {"short": short, "medium": medium, "long": long}

# Aturan fuzzy
rules = [
    {"risk": "low", "return": "high", "time": "short", "output": "Excellent"},
    {"risk": "low", "return": "medium", "time": "medium", "output": "Good"},
    {"risk": "medium", "return": "high", "time": "short", "output": "Good"},
    {"risk": "medium", "return": "medium", "time": "medium", "output": "Average"},
    {"risk": "high", "return": "low", "time": "long", "output": "Poor"},
    {"risk": "high", "return": "medium", "time": "long", "output": "Poor"},
]

# Logika fuzzy untuk keputusan investasi
def calculate_decision(risk_val, return_val, time_val):
    risk_membership = fuzzy_risk(risk_val)
    return_membership = fuzzy_return(return_val)
    time_membership = fuzzy_time(time_val)

    best_rule = None
    best_similarity = 0

    for rule in rules:
        similarity = min(
            risk_membership[rule["risk"]],
            return_membership[rule["return"]],
            time_membership[rule["time"]],
        )
        if similarity > best_similarity:
            best_similarity = similarity
            best_rule = rule

    return best_rule["output"] if best_rule else "No Result"

# GUI dengan Tkinter
def show_results():
    risk_val = slider_risk.get()
    return_val = slider_return.get()
    time_val = slider_time.get()

    result = calculate_decision(risk_val, return_val, time_val)
    result_label.config(text=f"Investment Decision: {result}")

    # Update grafik
    update_graph(risk_val, return_val, time_val)

def update_graph(risk_val, return_val, time_val):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Risiko
    x = range(0, 11)
    axs[0].plot(x, [fuzzy_risk(v)["low"] for v in x], label="Low", color="blue")
    axs[0].plot(x, [fuzzy_risk(v)["medium"] for v in x], label="Medium", color="green")
    axs[0].plot(x, [fuzzy_risk(v)["high"] for v in x], label="High", color="red")
    axs[0].axvline(x=risk_val, color="black", linestyle="--", label=f"Risk: {risk_val}")
    axs[0].set_title("Risk Membership")
    axs[0].legend()

    # Potensi pengembalian
    axs[1].plot(x, [fuzzy_return(v)["low"] for v in x], label="Low", color="blue")
    axs[1].plot(x, [fuzzy_return(v)["medium"] for v in x], label="Medium", color="green")
    axs[1].plot(x, [fuzzy_return(v)["high"] for v in x], label="High", color="red")
    axs[1].axvline(x=return_val, color="black", linestyle="--", label=f"Return: {return_val}")
    axs[1].set_title("Return Membership")
    axs[1].legend()

    # Jangka waktu
    axs[2].plot(x, [fuzzy_time(v)["short"] for v in x], label="Short", color="blue")
    axs[2].plot(x, [fuzzy_time(v)["medium"] for v in x], label="Medium", color="green")
    axs[2].plot(x, [fuzzy_time(v)["long"] for v in x], label="Long", color="red")
    axs[2].axvline(x=time_val, color="black", linestyle="--", label=f"Time: {time_val}")
    axs[2].set_title("Time Membership")
    axs[2].legend()

    canvas.figure = fig
    canvas.draw()

# Aplikasi GUI
app = tk.Tk()
app.title("Cryptocurrency Fuzzy Decision")
app.geometry("800x600")

# Sliders
tk.Label(app, text="Risk (0-10):").pack()
slider_risk = tk.Scale(app, from_=0, to=10, orient="horizontal")
slider_risk.pack()

tk.Label(app, text="Return Potential (0-10):").pack()
slider_return = tk.Scale(app, from_=0, to=10, orient="horizontal")
slider_return.pack()

tk.Label(app, text="Time Period (0-10):").pack()
slider_time = tk.Scale(app, from_=0, to=10, orient="horizontal")
slider_time.pack()

# Hasil
result_label = tk.Label(app, text="Investment Decision: ", font=("Helvetica", 14))
result_label.pack(pady=10)

tk.Button(app, text="Calculate", command=show_results).pack()

# Grafik
fig, _ = plt.subplots(1, 3, figsize=(15, 5))
canvas = FigureCanvasTkAgg(fig, master=app)
canvas.get_tk_widget().pack()

app.mainloop()
