from domain_models import db
from datetime import datetime


class SystemAdmin(db.Model):
    __tablename__ = "system_admins"

    adminId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    passwordHash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="ADMIN")

    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    # ===============================
    # METHODS (MATCHING CLASS DIAGRAM)
    # ===============================

    # View parent accounts (Requirement 27)
    def viewParentAccounts(self):
        from domain_models.parent_model import Parent
        return Parent.query.all()

    # Activate parent (Requirement 28)
    def activateParentAccount(self, parentId):
        from domain_models.parent_model import Parent

        parent = Parent.query.get(parentId)
        if parent:
            parent.profileStatus = "ACTIVE"
            db.session.commit()
            return True
        return False

    # Deactivate parent (Requirement 29)
    def deactivateParentAccount(self, parentId):
        from domain_models.parent_model import Parent

        parent = Parent.query.get(parentId)
        if parent:
            parent.profileStatus = "INACTIVE"
            db.session.commit()
            return True
        return False

    # ===============================
    # ROUTINE CATEGORY MANAGEMENT
    # ===============================

    def viewRoutineCategories(self):
        return RoutineCategory.query.all()

    def createRoutineCategory(self, label):
        category = RoutineCategory(label=label)
        db.session.add(category)
        db.session.commit()
        return category

    def updateRoutineCategory(self, categoryId, label):
        category = RoutineCategory.query.get(categoryId)
        if category:
            category.label = label
            db.session.commit()
            return True
        return False

    def removeRoutineCategory(self, categoryId):
        category = RoutineCategory.query.get(categoryId)
        if category:
            db.session.delete(category)
            db.session.commit()
            return True
        return False

    # ===============================
    # ALERT TEMPLATE MANAGEMENT
    # ===============================

    def viewAlertTemplates(self):
        return AlertTemplate.query.all()

    def updateAlertTemplates(self, templateId, message):
        template = AlertTemplate.query.get(templateId)
        if template:
            template.message = message
            db.session.commit()
            return True
        return False


# ===============================
# SUPPORT TABLES (FOR ADMIN)
# ===============================

class RoutineCategory(db.Model):
    __tablename__ = "routine_categories"

    categoryId = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), unique=True)


class AlertTemplate(db.Model):
    __tablename__ = "alert_templates"

    templateId = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))