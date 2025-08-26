import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Store history as a list of (weight, height, bmi)
bmi_history = []

def calculate_bmi(weight: float, height: float) -> float:
    return round(weight / (height ** 2), 2)

def get_bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal weight"
    elif bmi < 29.9:
        return "Overweight"
    return "Obese"

def calculate_and_display():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Weight and height must be positive.")
            return

        bmi = calculate_bmi(weight, height)
        category = get_bmi_category(bmi)

        result_label.config(text=f"BMI: {bmi} → {category}")

        # Save to history for graph (with weight and height for clarity)
        bmi_history.append((weight, height, bmi))

    except ValueError:
        messagebox.showerror("Error", "Please type valid numbers.")

def show_graph():
    if not bmi_history:
        messagebox.showinfo("No Data", "No BMI values calculated yet.")
        return
    
    # Extract BMI values for plotting
    bmi_values = [entry[2] for entry in bmi_history]

    plt.figure(figsize=(6,4))
    plt.plot(range(1, len(bmi_values)+1), bmi_values, marker="o", color="purple", linewidth=2)
    
    # Threshold lines
    plt.axhline(18.5, color="blue", linestyle="--", label="18.5 (Underweight/Normal)")
    plt.axhline(24.9, color="green", linestyle="--", label="24.9 (Normal/Overweight)")
    plt.axhline(29.9, color="red", linestyle="--", label="29.9 (Overweight/Obese)")

    plt.title("BMI Trend Over Time")
    plt.xlabel("Entry Number")
    plt.ylabel("BMI Value")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

# GUI setup
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x250")
root.config(bg="#e6f2ff")  # light blue background

# Labels and entries
tk.Label(root, text="Enter your weight (kg):", bg="#e6f2ff", font=("Arial", 11, "bold")).pack(pady=5)
weight_entry = tk.Entry(root, font=("Arial", 11))
weight_entry.pack()

tk.Label(root, text="Enter your height (m):", bg="#e6f2ff", font=("Arial", 11, "bold")).pack(pady=5)
height_entry = tk.Entry(root, font=("Arial", 11))
height_entry.pack()

# Buttons
tk.Button(root, text="Calculate BMI", command=calculate_and_display, 
          bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), relief="raised").pack(pady=10)

tk.Button(root, text="Show BMI Graph", command=show_graph, 
          bg="#2196F3", fg="white", font=("Arial", 11, "bold"), relief="raised").pack(pady=5)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#e6f2ff", fg="darkblue")
result_label.pack(pady=10)

root.mainloop()
