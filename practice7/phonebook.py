# phonebook.py
import csv
from connect import get_connection

# Connect to DB
connection, cursor = get_connection()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    contact_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    phone_number VARCHAR(20)
);
""")
connection.commit()

print("📒 Welcome to My PhoneBook 📒")

# 1. Add contact
def add_contact():
    name = input("Enter full name: ")
    phone = input("Enter phone number: ")
    cursor.execute(
        "INSERT INTO contacts (full_name, phone_number) VALUES (%s, %s)",
        (name, phone)
    )
    connection.commit()
    print("✅ Contact added!")

# 2. Update contact
def update_contact():
    old_name = input("Enter name to update: ")
    new_name = input("New name (leave empty to skip): ")
    new_phone = input("New phone (leave empty to skip): ")

    if new_name:
        cursor.execute(
            "UPDATE contacts SET full_name=%s WHERE full_name=%s",
            (new_name, old_name)
        )
    if new_phone:
        cursor.execute(
            "UPDATE contacts SET phone_number=%s WHERE full_name=%s",
            (new_phone, old_name)
        )

    connection.commit()
    print("✅ Updated!")

# 3. Show/Search contacts
def show_contacts():
    print("1. Show all")
    print("2. Search by name")
    print("3. Search by phone")

    choice = input("Choose: ")

    if choice == "1":
        cursor.execute("SELECT * FROM contacts")
    elif choice == "2":
        name = input("Enter name: ")
        cursor.execute(
            "SELECT * FROM contacts WHERE full_name ILIKE %s",
            ('%' + name + '%',)
        )
    elif choice == "3":
        prefix = input("Enter phone start: ")
        cursor.execute(
            "SELECT * FROM contacts WHERE phone_number LIKE %s",
            (prefix + '%',)
        )
    else:
        print("❌ Wrong choice")
        return

    data = cursor.fetchall()
    if not data:
        print("⚠️ No contacts found")
        return

    for row in data:
        print(f"{row[0]}. {row[1]} — {row[2]}")

# 4. Delete contact
def delete_contact():
    print("1. Delete by name")
    print("2. Delete by phone")

    choice = input("Choose: ")

    if choice == "1":
        name = input("Enter name: ")
        cursor.execute(
            "DELETE FROM contacts WHERE full_name=%s",
            (name,)
        )
    elif choice == "2":
        phone = input("Enter phone: ")
        cursor.execute(
            "DELETE FROM contacts WHERE phone_number=%s",
            (phone,)
        )
    else:
        print("❌ Wrong choice")
        return

    connection.commit()
    print("✅ Deleted!")

# 5. Import from CSV
def import_from_csv():
    filename = input("Enter CSV filename: ")
    try:
        with open(filename, newline='') as file:
            reader = csv.reader(file)
            count = 0
            for row in reader:
                if len(row) < 2:
                    continue
                name, phone = row
                cursor.execute(
                    "INSERT INTO contacts (full_name, phone_number) VALUES (%s, %s)",
                    (name, phone)
                )
                count += 1
        connection.commit()
        print(f"✅ {count} contacts imported!")
    except FileNotFoundError:
        print("❌ File not found!")

# 6. Export to CSV
def export_to_csv():
    filename = input("Enter CSV filename to save: ")
    cursor.execute("SELECT full_name, phone_number FROM contacts")
    rows = cursor.fetchall()
    if not rows:
        print("⚠️ No contacts to export")
        return

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

    print(f"✅ {len(rows)} contacts exported to {filename}")

# Menu
while True:
    print("\n--- MENU ---")
    print("1. Add contact")
    print("2. Update contact")
    print("3. Show/Search contacts")
    print("4. Delete contact")
    print("5. Import from CSV")
    print("6. Export to CSV")
    print("0. Exit")

    option = input("Select: ")

    if option == "1":
        add_contact()
    elif option == "2":
        update_contact()
    elif option == "3":
        show_contacts()
    elif option == "4":
        delete_contact()
    elif option == "5":
        import_from_csv()
    elif option == "6":
        export_to_csv()
    elif option == "0":
        print("👋 Bye!")
        break
    else:
        print("❌ Invalid option")

cursor.close()
connection.close()