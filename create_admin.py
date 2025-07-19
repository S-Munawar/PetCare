from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import os

# --- Configuration ---
# Make sure your MONGO_URI matches the one in your __init__.py
MONGO_URI = "mongodb://localhost:27017/petcare_db"
client = MongoClient(MONGO_URI)
db = client.get_database()
bcrypt = Bcrypt()


def create_admin_user():
    """
    A command-line tool to create the first admin user securely.
    """
    print("--- Create PetCare Admin User ---")

    # Check if an admin already exists
    if db.users.find_one({"is_admin": True}):
        print("\nAn admin account already exists. No new admin will be created.")
        return

    # Get admin details from user input
    username = input("Enter admin username: ").title()
    email = input("Enter admin email: ").lower()
    phone = input("Enter admin phone number: ")
    address = input("Enter admin address: ")
    password = input("Enter admin password: ")
    confirm_password = input("Confirm admin password: ")

    # Validate input
    if not all([username, email, password, phone, address]):
        print("\nError: All fields are required.")
        return

    if password != confirm_password:
        print("\nError: Passwords do not match.")
        return

    if db.users.find_one({"username": username}):
        print(f"\nError: Username '{username}' already exists.")
        return

    if db.users.find_one({"email": email}):
        print(f"\nError: Email '{email}' already exists.")
        return

    # Hash the password and create the admin user
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    admin_data = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "phone": phone,
        "address": address,
        "is_vet": False,
        "is_admin": True  # Set the admin flag
    }

    db.users.insert_one(admin_data)
    print(f"\nAdmin user '{username}' created successfully!")
    print("You can now log in using the main /login route.")


if __name__ == "__main__":
    create_admin_user()
