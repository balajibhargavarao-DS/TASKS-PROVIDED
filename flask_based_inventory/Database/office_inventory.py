import sqlite3

conn = sqlite3.connect("office_inventory.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT,
    description TEXT,
    quantity INTEGER,
    location TEXT
)
""")

inventory_data = [
    ("Laptop – Dell Latitude 5420", "Standard employee laptop", 12, "IT Store"),
    ("Laptop – HP EliteBook 840", "Manager-grade laptop", 5, "IT Store"),
    ("Desktop PC – Lenovo ThinkCentre", "Office desk PC", 9, "Workstations"),
    ("Monitor – Dell 24 inch", "External display", 15, "IT Store"),
    ("Keyboard – Logitech Wireless", "Wireless keyboard", 20, "IT Cabinet"),
    ("Mouse – Logitech M235", "Wireless mouse", 25, "IT Cabinet"),
    ("Projector – Sony", "Meeting room projector", 2, "Conference Room"),
    ("HDMI Cable", "Laptop connectivity", 30, "IT Cabinet"),
    ("Headset – Jabra", "For calls/meetings", 10, "IT Store"),
    ("WiFi Router – TP-Link", "Networking equipment", 3, "Server Room")
]

cur.executemany(
    "INSERT INTO inventory (item, description, quantity, location) VALUES (?, ?, ?, ?)",
    inventory_data
)

conn.commit()
conn.close()

print("Office Inventory Database created successfully!")