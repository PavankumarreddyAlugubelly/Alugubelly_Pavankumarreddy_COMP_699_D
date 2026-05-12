from datetime import datetime
from domain_models import db


class DailyActivity(db.Model):
    __tablename__ = "daily_activities"

    activityId = db.Column(db.Integer, primary_key=True)

    studyTime = db.Column(db.Integer, nullable=False)
    sleepDuration = db.Column(db.Integer, nullable=False)
    screenTime = db.Column(db.Integer, nullable=False)
    spendingFrequency = db.Column(db.Integer, nullable=False)

    activityDate = db.Column(db.DateTime, default=datetime.utcnow)

    childId = db.Column(db.Integer, db.ForeignKey("child_profiles.childId"), nullable=False)

    # ===============================
    # METHOD (MATCHING CLASS DIAGRAM)
    # ===============================

    def validate(self):
        if self.studyTime < 0 or self.sleepDuration < 0 or self.screenTime < 0:
            return False
        if self.spendingFrequency < 0:
            return False
        return True