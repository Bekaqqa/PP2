# phonebook.py
import csv
from connect import get_connection

# Connect to DB
connection, cursor = get_connection()

# Table creation
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    contact_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    phone_number VARCHAR(20)
);
""")
connection.commit()

print("📒 Welcome to My PhoneBook (Practice 8) 📒")


# 🔁 1. Add / Update (через PROCEDURE)
def add_contact():
    name = input("Enter full name: ")
    phone = input("Enter phone number: ")

    cursor.execute("CALL upsert_contact(%s, %s)", (name, phone))
    connection.commit()

    print("✅ Added or updated!")


# 🔍 2. Search (через FUNCTION)
def show_contacts():
    pattern = input("Enter search: ")

    cursor.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cursor.fetchall()

    if not rows:
        print("No contacts found")
        return

    for row in rows:
        print(f"{row[0]}. {row[1]} — {row[2]}")


# ❌ 3. Delete (через PROCEDURE)
def delete_contact():
    value = input("Enter name or phone: ")

    cursor.execute("CALL delete_contact(%s)", (value,))
    connection.commit()

    print("✅ Deleted!")


# 📄 4. Pagination (через FUNCTION)
def show_paginated():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    cursor.execute(
        "SELECT * FROM get_contacts_paginated(%s, %s)",
        (limit, offset)
    )

    rows = cursor.fetchall()

    if not rows:
        print("No data")
        return

    for row in rows:
        print(f"{row[0]}. {row[1]} — {row[2]}")


# 📦 5. Bulk insert (через PROCEDURE)
def insert_many():
    n = int(input("How many contacts: "))

    names = []
    phones = []

    for i in range(n):
        name = input(f"Name {i+1}: ")
        phone = input(f"Phone {i+1}: ")

        names.append(name)
        phones.append(phone)

    cursor.execute(
        "CALL insert_many(%s, %s)",
        (names, phones)
    )
    connection.commit()

    print("✅ Bulk insert done (check NOTICE for errors)")


# 📥 6. Import from CSV (теперь через bulk)
def import_from_csv():
    filename = input("Enter CSV filename: ")

    try:
        names = []
        phones = []

        with open(filename, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 2:
                    continue
                names.append(row[0])
                phones.append(row[1])

        cursor.execute(
            "CALL insert_many(%s, %s)",
            (names, phones)
        )
        connection.commit()

        print("✅ Imported via procedure!")

    except FileNotFoundError:
        print("❌ File not found!")


# 📤 7. Export (оставляем как есть)
def export_to_csv():
    filename = input("Enter CSV filename to save: ")

    cursor.execute("SELECT full_name, phone_number FROM contacts")
    rows = cursor.fetchall()

    if not rows:
        print("⚠️ No contacts to export")
        return

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"✅ {len(rows)} contacts exported to {filename}")


# 🧾 MENU
while True:
    print("\n--- MENU ---")
    print("1. Add / Update contact")
    print("2. Search contacts")
    print("3. Delete contact")
    print("4. Show paginated")
    print("5. Bulk insert")
    print("6. Import from CSV")
    print("7. Export to CSV")
    print("0. Exit")

    option = input("Select: ")

    if option == "1":
        add_contact()
    elif option == "2":
        show_contacts()
    elif option == "3":
        delete_contact()
    elif option == "4":
        show_paginated()
    elif option == "5":
        insert_many()
    elif option == "6":
        import_from_csv()
    elif option == "7":
        export_to_csv()
    elif option == "0":
        print("Bye!")
        break
    else:
        print("❌ Invalid option")


cursor.close()
connection.close()