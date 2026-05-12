from datetime import datetime
from domain_models import db


class Alert(db.Model):
    __tablename__ = "alerts"

    alertId = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.String(50), nullable=False)

    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    parentId = db.Column(db.Integer, db.ForeignKey("parents.parentId"), nullable=False)

    # ===============================
    # METHOD (MATCHING CLASS DIAGRAM)
    # ===============================

    @staticmethod
    def createAlert(parentId, message, severity):
        alert = Alert(
            parentId=parentId,
            message=message,
            severity=severity
        )
        db.session.add(alert)
        db.session.commit()
        return alert