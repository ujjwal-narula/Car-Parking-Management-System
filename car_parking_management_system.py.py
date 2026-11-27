import pymysql

# ---------- Connect to the database ----------
password = input("Enter MySQL root password: ")
try:
    db = pymysql.connect(
        host="localhost",
        user="root",
        password=password,
        database="CPMS"
    )
except pymysql.Error as e:
    print("Could not connect to MySQL:", e)
    exit()
cursor = db.cursor()

VALID_TYPES = ("compact", "large", "EV")


def ask_type(prompt):
    t = input(prompt).strip()
    for valid in VALID_TYPES:
        if t.lower() == valid.lower():
            return valid
    return None


def add_parking_slot():
    slot_number = input("Enter slot number: ").strip().upper()
    level = input("Enter level (number): ").strip()
    slot_type = ask_type("Enter slot type (compact/large/EV): ")

    if slot_number == "" or not level.isdigit() or slot_type is None:
        print("Invalid input. Slot not added.")
        return
    try:
        cursor.execute(
            "INSERT INTO ParkingSlot (slot_number, level, is_occupied, slot_type) VALUES (%s, %s, 0, %s)",
            (slot_number, int(level), slot_type)
        )
        db.commit()
        print("Slot added successfully.")
    except pymysql.Error:
        db.rollback()
        print("Slot number already exists or data is invalid.")


def register_vehicle():
    vehicle_id = input("Enter vehicle number (e.g. DL01AB1234): ").strip().upper()
    owner = input("Enter owner name: ").strip()
    phone = input("Enter phone number: ").strip()
    v_type = ask_type("Enter vehicle type (compact/large/EV): ")

    if vehicle_id == "" or owner == "" or v_type is None:
        print("Invalid input. Vehicle not registered.")
        return
    if phone != "" and (not phone.isdigit() or len(phone) != 10):
        print("Phone number must be 10 digits.")
        return
    try:
        cursor.execute(
            "INSERT INTO Vehicle (vehicle_id, owner_name, phone, vehicle_type) VALUES (%s, %s, %s, %s)",
            (vehicle_id, owner, phone, v_type)
        )
        db.commit()
        print("Vehicle registered successfully.")
    except pymysql.Error:
        db.rollback()
        print("This vehicle is already registered.")


def park_vehicle():
    vehicle_id = input("Enter vehicle ID: ").strip().upper()

    cursor.execute("SELECT vehicle_type FROM Vehicle WHERE vehicle_id = %s", (vehicle_id,))
    vehicle = cursor.fetchone()
    if not vehicle:
        print("Vehicle not registered. Please register it first (option 2).")
        return

    cursor.execute(
        "SELECT record_id FROM ParkingRecord WHERE vehicle_id = %s AND exit_time IS NULL",
        (vehicle_id,)
    )
    if cursor.fetchone():
        print("This vehicle is already parked.")
        return

    cursor.execute(
        "SELECT slot_id, slot_number FROM ParkingSlot "
        "WHERE is_occupied = 0 AND slot_type = %s ORDER BY level, slot_number LIMIT 1",
        (vehicle[0],)
    )
    slot = cursor.fetchone()

    if slot:
        slot_id, slot_number = slot
        try:
            cursor.execute(
                "INSERT INTO ParkingRecord (vehicle_id, slot_id, entry_time) VALUES (%s, %s, NOW())",
                (vehicle_id, slot_id)
            )
            cursor.execute("UPDATE ParkingSlot SET is_occupied = 1 WHERE slot_id = %s", (slot_id,))
            db.commit()
            print(f"Vehicle {vehicle_id} parked in slot {slot_number}.")
        except pymysql.Error:
            db.rollback()
            print("Error while parking the vehicle.")
    else:
        print(f"No available {vehicle[0]} slots.")


def release_vehicle():
    vehicle_id = input("Enter vehicle ID to release: ").strip().upper()
    cursor.execute(
        "SELECT r.record_id, r.slot_id, s.slot_type, "
        "GREATEST(1, CEIL(TIMESTAMPDIFF(MINUTE, r.entry_time, NOW()) / 60)) "
        "FROM ParkingRecord r JOIN ParkingSlot s ON r.slot_id = s.slot_id "
        "WHERE r.vehicle_id = %s AND r.exit_time IS NULL",
        (vehicle_id,)
    )
    record = cursor.fetchone()

    if record:
        record_id, slot_id, slot_type, hours = record
        cursor.execute("SELECT rate_per_hour FROM RateCard WHERE slot_type = %s", (slot_type,))
        rate = cursor.fetchone()[0]
        fee = float(rate) * int(hours)
        try:
            cursor.execute(
                "UPDATE ParkingRecord SET exit_time = NOW(), fee = %s WHERE record_id = %s",
                (fee, record_id)
            )
            cursor.execute("UPDATE ParkingSlot SET is_occupied = 0 WHERE slot_id = %s", (slot_id,))
            db.commit()
            print(f"Vehicle released. Hours charged: {hours} | Rate: Rs.{rate}/hr | Fee: Rs.{fee}")
        except pymysql.Error:
            db.rollback()
            print("Error while releasing the vehicle.")
    else:
        print("No active record found for this vehicle.")


def view_parking_status():
    cursor.execute("SELECT slot_number, level, is_occupied, slot_type FROM ParkingSlot ORDER BY level, slot_number")
    rows = cursor.fetchall()
    print("\nParking Status")
    free = 0
    for slot_number, level, is_occupied, slot_type in rows:
        status = "Occupied" if is_occupied else "Available"
        if not is_occupied:
            free += 1
        print(f"Slot: {slot_number} | Level: {level} | Type: {slot_type} | Status: {status}")
    print(f"Total slots: {len(rows)} | Available: {free} | Occupied: {len(rows) - free}")


def view_parked_vehicles():
    cursor.execute(
        "SELECT v.vehicle_id, v.owner_name, s.slot_number, r.entry_time "
        "FROM ParkingRecord r JOIN Vehicle v ON r.vehicle_id = v.vehicle_id "
        "JOIN ParkingSlot s ON r.slot_id = s.slot_id WHERE r.exit_time IS NULL"
    )
    rows = cursor.fetchall()
    print("\nCurrently Parked Vehicles")
    if not rows:
        print("No vehicles parked right now.")
    for vehicle_id, owner, slot_number, entry in rows:
        print(f"Vehicle: {vehicle_id} | Owner: {owner} | Slot: {slot_number} | Entry: {entry}")


def view_history():
    cursor.execute(
        "SELECT vehicle_id, slot_id, entry_time, exit_time, fee FROM ParkingRecord "
        "WHERE exit_time IS NOT NULL ORDER BY exit_time DESC"
    )
    rows = cursor.fetchall()
    print("\nParking History")
    total = 0
    if not rows:
        print("No completed records yet.")
    for vehicle_id, slot_id, entry, exit_time, fee in rows:
        print(f"Vehicle: {vehicle_id} | Entry: {entry} | Exit: {exit_time} | Fee: Rs.{fee}")
        total += float(fee)
    print(f"Total collection: Rs.{total}")


# ---------- Main Menu Loop ----------
while True:
    print("\n===== CAR PARKING MANAGEMENT SYSTEM =====")
    print("1. Add Parking Slot")
    print("2. Register Vehicle")
    print("3. Park Vehicle")
    print("4. Release Vehicle")
    print("5. View Parking Status")
    print("6. View Currently Parked Vehicles")
    print("7. View Parking History")
    print("8. Exit")

    choice = input("Enter choice: ").strip()

    if choice == '1':
        add_parking_slot()
    elif choice == '2':
        register_vehicle()
    elif choice == '3':
        park_vehicle()
    elif choice == '4':
        release_vehicle()
    elif choice == '5':
        view_parking_status()
    elif choice == '6':
        view_parked_vehicles()
    elif choice == '7':
        view_history()
    elif choice == '8':
        break
    else:
        print("Invalid choice.")

cursor.close()
db.close()
print("Goodbye!")
