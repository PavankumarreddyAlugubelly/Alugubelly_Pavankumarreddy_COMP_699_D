from domain_models import db
from domain_models.parent_model import Parent
from domain_models.admin_model import SystemAdmin
from werkzeug.security import generate_password_hash, check_password_hash


class AuthService:

    # Register Parent (Req 1)
    @staticmethod
    def register_parent(email, password):
        if Parent.query.filter_by(email=email).first():
            return None, "Email already exists"

        parent = Parent(
            email=email,
            passwordHash=generate_password_hash(password)
        )

        db.session.add(parent)
        db.session.commit()
        return parent, "Registered successfully"

    # Login Parent (Req 2)
    @staticmethod
    def login_parent(email, password):
        parent = Parent.query.filter_by(email=email).first()

        if not parent:
            return None, "User not found"

        if not check_password_hash(parent.passwordHash, password):
            return None, "Invalid password"

        if parent.profileStatus == "INACTIVE":
            return None, "Account is deactivated"

        return parent, "Login successful"

    # Admin Login (Req 26)
    @staticmethod
    def login_admin(username, password):
        admin = SystemAdmin.query.filter_by(username=username).first()

        if not admin:
            return None, "Admin not found"

        if not check_password_hash(admin.passwordHash, password):
            return None, "Invalid credentials"

        return admin, "Admin login successful"

    # Password Reset (Req 5 - simplified)
    @staticmethod
    def reset_password(email, new_password):
        parent = Parent.query.filter_by(email=email).first()

        if not parent:
            return False

        parent.passwordHash = generate_password_hash(new_password)
        db.session.commit()
        return True