import tkinter as tk
from tkinter import messagebox

def calculate_pay():
    try:
        rate = float(entry_rate.get())
        hours = float(entry_hours.get())
        total = rate * hours
        result_label.config(text=f"Total Pay: £{total:.2f}")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers.")

# Setup UI
window = tk.Tk()
window.title("Care Home Hourly Pay Calculator")

tk.Label(window, text="Department:").grid(row=0, column=0)
entry_dept = tk.Entry(window)
entry_dept.grid(row=0, column=1)

tk.Label(window, text="Hourly Rate (£):").grid(row=1, column=0)
entry_rate = tk.Entry(window)
entry_rate.grid(row=1, column=1)

tk.Label(window, text="Total Hours:").grid(row=2, column=0)
entry_hours = tk.Entry(window)
entry_hours.grid(row=2, column=1)

tk.Button(window, text="Calculate", command=calculate_pay).grid(row=3, column=0, columnspan=2)

result_label = tk.Label(window, text="Total Pay: £0.00", fg="green")
result_label.grid(row=4, column=0, columnspan=2)

window.mainloop()
