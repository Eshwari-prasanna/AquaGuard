# 💧 AquaGuard – Smart Water Usage Monitor

AquaGuard is a **Python-based GUI application** built using **Tkinter** that helps users monitor, manage, and analyze their **daily water consumption**. It supports adding, updating, and deleting records, and provides an automatic **bill estimation** and **usage summary report**.

---

## 🚀 Features

- 📅 **Record Management** – Add, update, and delete daily water usage entries  
- 💧 **Usage Monitoring** – View total consumption and usage category  
- 💰 **Bill Estimation** – Automatically calculates an estimated bill based on water usage  
- 📊 **Daily Report Generation** – Summarizes daily usage and flags over-consumption days  
- 💾 **Persistent Storage** – Saves data locally in a JSON file (`storage.json`)  
- 🧮 **Real-Time Summary** – Displays total records and overall water usage  

---

## 🧠 How It Works

1. The app loads previous records from `storage.json` on startup.  
2. You can enter:
   - Date (format: `YYYY-MM-DD`)
   - Water usage (in litres)
   - Category (Domestic / Commercial)
3. Each entry automatically calculates the estimated bill (default: ₹0.02 per litre).
4. You can update or delete selected entries from the table.
5. Click **“Generate Report”** to view daily usage and any threshold alerts (default threshold: 500L/day).

---
## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AquaGuard
## 📁 Project Structure 
AquaGuard/
│
├── storage.json      # Stores user records (auto-created)
├── aquaguard.py      # Main Tkinter application
└── README.md         # Project documentation
