from datetime import datetime
from bson.objectid import ObjectId
from flask_login import UserMixin
from petcare import mongo, bcrypt, login_manager

class User(UserMixin):
    """
    Represents a user in the system, who can be a pet owner, a vet, or an admin.
    """
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data["username"]
        self.email = user_data["email"]
        self.password = user_data["password"]
        self.phone = user_data.get("phone")
        self.address = user_data.get("address")
        self.is_admin = user_data.get("is_admin", False)
        self.verified = user_data.get("verified", False)
        # Vet-specific fields
        self.is_vet = user_data.get("is_vet", False)
        self.vet_license = user_data.get("vet_license")
        self.qualification = user_data.get("qualification")

    @staticmethod
    def get(user_id):
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return User(user_data) if user_data else None

    def get_pets(self):
        """Retrieves all pets associated with this user."""
        return list(mongo.db.pets.find({"owner_id": ObjectId(self.id)}))

    def check_password(self, attempted_password):
        """Verifies the user's password."""
        return bcrypt.check_password_hash(self.password, attempted_password)

class Pet:
    """
    Represents a pet's profile and provides methods to access related data.
    """
    @staticmethod
    def get_by_id(pet_id):
        return mongo.db.pets.find_one({"_id": ObjectId(pet_id)})

    @staticmethod
    def get_health_history(pet_id):
        return list(mongo.db.health_reports.find({"pet_id": ObjectId(pet_id)}).sort("report_date", -1))

class HealthReport:
    """
    Handles the creation of health reports.
    """
    @staticmethod
    def create(pet_id, input_data, prediction_result, vet_id=None):
        report_data = {
            "pet_id": ObjectId(pet_id),
            "report_date": datetime.utcnow(),
            "input_data": input_data,
            "prediction_result": prediction_result
        }
        if vet_id:
            report_data["diagnosed_by_vet_id"] = ObjectId(vet_id)
        return mongo.db.health_reports.insert_one(report_data)

class VetLicense:
    """
    Handles validation of veterinarian licenses.
    """
    @staticmethod
    def get(vet_license):
        return mongo.db.vetlicenses.find_one({"vet_license": vet_license})

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login helper function to load a user from the database."""
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(user_data) if user_data else None