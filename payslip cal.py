import tkinter as tk
from tkinter import ttk, messagebox
import csv
from tkinter import filedialog
import datetime

departments = ["Senior", "Carer", "Cleaning", "Kitchen", "Admin"]
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
entries = []
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def get_mondays_in_month(month_name, year=2025):
    month_number = months.index(month_name) + 1
    first_day = datetime.date(year, month_number, 1)
    last_day = datetime.date(year, month_number + 1, 1) - datetime.timedelta(days=1) if month_number < 12 else datetime.date(year, 12, 31)

    mondays = []
    current_day = first_day
    while current_day <= last_day:
        if current_day.weekday() == 0:
            mondays.append(current_day.strftime("%Y-%m-%d"))
        current_day += datetime.timedelta(days=1)
    return mondays

def get_pay_period_month(week_start_str):
    week_start = datetime.datetime.strptime(week_start_str, "%Y-%m-%d").date()
    if week_start.day >= 28:
        next_month = (week_start.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
        return next_month.strftime("%B")
    else:
        return week_start.strftime("%B")

def update_week_dropdown(event=None):
    selected_month = month_var.get()
    if selected_month:
        weeks = get_mondays_in_month(selected_month)
        week_start_dropdown['values'] = weeks
        if weeks:
            week_start_var.set(weeks[0])
        else:
            week_start_var.set('')

def calculate_weekly_hours():
    try:
        total = 0.0
        for d in days:
            val = day_entries[d].get()
            if val.strip() != "":
                total += float(val)
        weekly_total_label.config(text=f"Weekly Total Hours: {total:.2f}")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers for daily hours.")

def add_entry():
    name = entry_name.get()
    dept = dept_var.get()
    week_start = week_start_var.get()
    if not week_start:
        messagebox.showerror("Missing input", "Please select a Week Starting date.")
        return

    try:
        rate = float(entry_rate.get())
        daily_hours = []
        for d in days:
            value = day_entries[d].get()
            if value.strip() == "":
                daily_hours.append(0.0)
            else:
                try:
                    daily_hours.append(float(value))
                except ValueError:
                    messagebox.showerror("Invalid input", f"Enter a number for {d} or leave it blank.")
                    return

        weekly_hours = sum(daily_hours)
        weekly_pay = rate * weekly_hours
        pay_period = get_pay_period_month(week_start)

        entry = {
            "name": name,
            "dept": dept,
            "pay_period": pay_period,
            "week_start": week_start,
            "rate": rate,
            "weekly_hours": weekly_hours,
            "weekly_pay": weekly_pay
        }

        entries.append(entry)

        tree.insert('', 'end', values=(
            name, dept, week_start, pay_period,
            f"£{rate:.2f}",
            f"{weekly_hours:.1f}",
            f"£{weekly_pay:.2f}"
        ))

        entry_name.delete(0, tk.END)
        entry_rate.delete(0, tk.END)
        for e in day_entries.values():
            e.delete(0, tk.END)
        calculate_weekly_hours()

    except ValueError:
        messagebox.showerror("Invalid input", "Please enter numeric values only.")

def generate_monthly_summary():
    summary = {}

    for e in entries:
        key = f"{e['pay_period']} - {e['dept']}"
        summary.setdefault(key, {
            "pay_period": e['pay_period'],
            "department": e['dept'],
            "total_hours": 0.0,
            "total_pay": 0.0
        })
        summary[key]["total_hours"] += e["weekly_hours"]
        summary[key]["total_pay"] += e["weekly_pay"]

    return list(summary.values())

def export_summary_to_csv():
    summary_data = generate_monthly_summary()
    if not summary_data:
        messagebox.showinfo("No data", "No summary data to export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

    if file_path:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Pay Period", "Department", "Total Hours", "Total Pay (£)"])
            for item in summary_data:
                writer.writerow([
                    item["pay_period"],
                    item["department"],
                    f"{item['total_hours']:.1f}",
                    f"{item['total_pay']:.2f}"
                ])
        messagebox.showinfo("Export Successful", f"Summary exported to:\n{file_path}")


def calculate_summary():
    if not entries:
        messagebox.showinfo("No entries", "Please add entries first.")
        return

    summary = {}

    for e in entries:
        key = f"{e['pay_period']} - {e['dept']}"
        summary.setdefault(key, {
            "weekly_hours": 0, "weekly_pay": 0
        })
        summary[key]["weekly_hours"] += e["weekly_hours"]
        summary[key]["weekly_pay"] += e["weekly_pay"]

    summary_str = ""
    for key, data in summary.items():
        summary_str += (
            f"{key}:\n"
            f"  Total Hours: {data['weekly_hours']:.1f}\n"
            f"  Total Pay: £{data['weekly_pay']:.2f}\n\n"
        )

    total_pay = sum(d['weekly_pay'] for d in summary.values())
    summary_str += f"Overall Pay: £{total_pay:.2f}"
    messagebox.showinfo("Monthly Pay Summary", summary_str)

# GUI Setup
window = tk.Tk()
window.title("Care Home Pay Calculator - Pay Period Breakdown")

tk.Label(window, text="Employee Name:").grid(row=0, column=0)
entry_name = tk.Entry(window)
entry_name.grid(row=0, column=1)

tk.Label(window, text="Department:").grid(row=1, column=0)
dept_var = tk.StringVar()
dept_dropdown = ttk.Combobox(window, textvariable=dept_var, values=departments, state="readonly")
dept_dropdown.grid(row=1, column=1)
dept_dropdown.current(0)

tk.Label(window, text="Month:").grid(row=2, column=0)
month_var = tk.StringVar()
month_dropdown = ttk.Combobox(window, textvariable=month_var, values=months, state="readonly")
month_dropdown.grid(row=2, column=1)
month_dropdown.bind("<<ComboboxSelected>>", update_week_dropdown)
month_dropdown.current(0)

tk.Label(window, text="Week Starting:").grid(row=3, column=0)
week_start_var = tk.StringVar()
week_start_dropdown = ttk.Combobox(window, textvariable=week_start_var, state="readonly")
week_start_dropdown.grid(row=3, column=1)

tk.Label(window, text="Hourly Rate (£):").grid(row=4, column=0)
entry_rate = tk.Entry(window)
entry_rate.grid(row=4, column=1)

# Daily inputs
day_entries = {}
for i, day in enumerate(days):
    tk.Label(window, text=f"{day} Hours:").grid(row=5+i, column=0)
    e = tk.Entry(window)
    e.grid(row=5+i, column=1)
    day_entries[day] = e

tk.Button(window, text="Add Entry", command=add_entry).grid(row=12, column=0, columnspan=2, pady=5)

weekly_total_label = tk.Label(window, text="Weekly Total Hours: 0.0", fg="blue")
weekly_total_label.grid(row=13, column=0, columnspan=2)

tk.Button(window, text="Calculate Weekly Hours", command=calculate_weekly_hours).grid(row=14, column=0, columnspan=2, pady=5)

# Table
columns = (
    "Name", "Department", "Week Starting", "Pay Period", "Hourly Rate",
    "Weekly Hours", "Weekly Pay"
)
tree = ttk.Treeview(window, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=115)
tree.grid(row=15, column=0, columnspan=2, padx=10, pady=10)

tk.Button(window, text="Calculate Summary", command=calculate_summary).grid(row=16, column=0, columnspan=2, pady=5)

tk.Button(window, text="Export Summary to CSV", command=export_summary_to_csv).grid(row=16, column=1, columnspan=2, pady=5)

update_week_dropdown()
window.mainloop()
