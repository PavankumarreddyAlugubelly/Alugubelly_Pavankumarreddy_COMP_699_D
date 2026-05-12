from main import create_app
from domain_models import db
from domain_models.admin_model import SystemAdmin
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():

    existing_admin = SystemAdmin.query.filter_by(
        username="admin@alugubellytech.com"
    ).first()

    if existing_admin:
        print("Admin already exists.")
    else:
        admin = SystemAdmin(
            username="admin@alugubellytech.com",
            passwordHash=generate_password_hash("admin123"),  
            role="SUPER_ADMIN"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully!")