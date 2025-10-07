import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

DATA_FILE = "storage.json"

# ---------- Helper Functions ----------

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def calculate_summary(data):
    total_usage = sum(entry["usage"] for entry in data)
    return f"Total Records: {len(data)} | Total Usage: {total_usage} L"

def estimate_bill(usage):
    rate_per_litre = 0.02  # Example rate
    return round(usage * rate_per_litre, 2)

# ---------- GUI Class ----------

class AquaGuardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AquaGuard – Smart Water Usage Monitor")
        self.data = load_data()
        
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # Input Frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Usage (litres):").grid(row=1, column=0)
        self.usage_entry = tk.Entry(input_frame)
        self.usage_entry.grid(row=1, column=1)

        tk.Label(input_frame, text="Category (Domestic/Commercial):").grid(row=2, column=0)
        self.category_entry = tk.Entry(input_frame)
        self.category_entry.grid(row=2, column=1)

        tk.Button(input_frame, text="Add Entry", command=self.add_entry).grid(row=3, column=0, pady=5)
        tk.Button(input_frame, text="Update Selected", command=self.update_entry).grid(row=3, column=1)
        tk.Button(input_frame, text="Delete Selected", command=self.delete_entry).grid(row=3, column=2)

        # Treeview
        self.tree = ttk.Treeview(self.root, columns=("Date", "Usage", "Category", "Bill"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        # Summary
        self.summary_label = tk.Label(self.root, text="", font=('Arial', 12))
        self.summary_label.pack()

        # Reports
        report_btn = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        report_btn.pack(pady=5)

    def add_entry(self):
        date = self.date_entry.get()
        usage = self.usage_entry.get()
        category = self.category_entry.get()

        if not (date and usage and category):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            usage = float(usage)
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date or usage format.")
            return

        entry = {
            "date": date,
            "usage": usage,
            "category": category,
            "bill": estimate_bill(usage)
        }
        self.data.append(entry)
        save_data(self.data)
        self.refresh_table()

    def update_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "No entry selected.")
            return

        idx = self.tree.index(selected[0])
        date = self.date_entry.get()
        usage = self.usage_entry.get()
        category = self.category_entry.get()

        try:
            usage = float(usage)
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")
            return

        self.data[idx] = {
            "date": date,
            "usage": usage,
            "category": category,
            "bill": estimate_bill(usage)
        }
        save_data(self.data)
        self.refresh_table()

    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "No entry selected.")
            return
        idx = self.tree.index(selected[0])
        del self.data[idx]
        save_data(self.data)
        self.refresh_table()

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for entry in self.data:
            self.tree.insert('', 'end', values=(entry["date"], entry["usage"], entry["category"], f"${entry['bill']}"))
        self.summary_label.config(text=calculate_summary(self.data))

    def generate_report(self):
        daily = {}
        for entry in self.data:
            day = entry["date"]
            daily[day] = daily.get(day, 0) + entry["usage"]

        report = "Daily Usage Report:\n"
        for day, usage in sorted(daily.items()):
            report += f"{day}: {usage} L\n"

        # Threshold example
        threshold = 500
        alert_days = [d for d, u in daily.items() if u > threshold]

        if alert_days:
            report += "\n⚠ Threshold Alert Days (>500L):\n"
            report += "\n".join(alert_days)

        messagebox.showinfo("Report", report)


# ---------- Main ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = AquaGuardApp(root)
    root.mainloop()

