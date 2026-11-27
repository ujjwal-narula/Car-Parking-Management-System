# 🚗 Car Parking Management System (CPMS)

A menu-driven **Python + MySQL** application that automates parking operations: slot allocation, vehicle registration, fee calculation and live reports. Built as a collaborative project for **Computational Thinking and Programming (2026CSAE100)** at Bennett University, Greater Noida.

---

## 📌 Problem
Parking in campuses, malls and offices is often managed with registers or paper slips. This causes slow entries, double-allotted slots, lost records and wrong fees. CPMS replaces this with a database-backed system that is fast, accurate and keeps a permanent history.

## ✨ Features
- **Add parking slots** – slot number, level and type (compact / large / EV)
- **Register vehicles** – registration number, owner, 10-digit phone, vehicle type
- **Smart slot allocation** – first free slot of the *matching type*, lowest level first
- **Double-parking prevention** – a vehicle cannot be parked twice
- **Automatic fee calculation** – rounded up to the next hour, minimum 1 hour, rate by slot type
- **Live reports** – slot status with available/occupied counts, currently parked vehicles, parking history with total collection
- **Input validation and safe error handling** – `try / except` with `rollback`

## 🛠️ Tech Stack
| Component | Details |
|---|---|
| Language | Python 3.x |
| Database | MySQL 8.0 |
| Connector | PyMySQL (only external module used) |

## 🗄️ Database Design (`CPMS`)
| Table | Purpose |
|---|---|
| `ParkingSlot` | Slot number, level, type, occupied flag |
| `Vehicle` | Registration number, owner name, phone, vehicle type |
| `RateCard` | Hourly rate per slot type (compact ₹20, large ₹40, EV ₹30) |
| `ParkingRecord` | Entry time, exit time and fee for each visit (foreign keys to slot and vehicle) |

## 📁 Project Structure
```
CPMS/
├── car_parking_management_system.py   # Main Python program
├── cpms_database.sql                  # Creates database, tables and sample data
└── README.md
```

## ⚙️ Setup and Run
1. **Install MySQL 8.0** and note your root password.
2. **Install PyMySQL:**
   ```
   pip install pymysql
   ```
3. **Create the database** (run once). In MySQL Command Line Client:
   ```
   source C:/path/to/cpms_database.sql;
   ```
   Use forward slashes `/` in the path.
4. **Run the program:**
   ```
   python car_parking_management_system.py
   ```
5. Enter your MySQL root password when asked.

> The password is typed at runtime and is never stored in the code.

## 🖥️ Menu
```
===== CAR PARKING MANAGEMENT SYSTEM =====
1. Add Parking Slot
2. Register Vehicle
3. Park Vehicle
4. Release Vehicle
5. View Parking Status
6. View Currently Parked Vehicles
7. View Parking History
8. Exit
```

### Sample Output
```
Vehicle DL01AB1234 parked in slot A1.
Vehicle released. Hours charged: 1 | Rate: Rs.20.00/hr | Fee: Rs.20.0
```

## 🧮 Fee Formula
```
hours = max(1, ceil(minutes_parked / 60))
fee   = hours × rate_per_hour (by slot type)
```
Example: a compact car parked for 2 h 10 min is charged 3 × ₹20 = ₹60.

## 🐍 Python Concepts Used
Variables and data types, conditional statements, loops, tuples, user-defined functions, exception handling, string methods, and database connectivity with PyMySQL (parameterised queries, `commit`, `rollback`).

## 🔮 Future Improvements
- Graphical interface (Tkinter) or web interface
- Printed / PDF receipts
- IoT sensors and number-plate recognition
- Online booking and payment
- Revenue and occupancy analytics

## 👥 Team
| Name | Role |
|---|---|
| **Ujjwal Narula** | Team Lead – program and database design, development |
| **Pakhi Singh** | Debugging and testing |
| **Wamika** | Documentation, flowcharts and presentation |

**Faculty Guide:** Dr. Pooja
**Institution:** Bennett University, Greater Noida, Uttar Pradesh
**Programme:** B.Tech. Mechanical Engineering (Batch 1), School of Engineering and Applied Sciences

## 📄 Note
This is an academic project created for learning purposes.
