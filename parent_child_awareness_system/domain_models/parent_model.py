from datetime import datetime
from domain_models import db


class Parent(db.Model):
    __tablename__ = "parents"

    parentId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwordHash = db.Column(db.String(255), nullable=False)
    profileStatus = db.Column(db.String(50), default="ACTIVE")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    children = db.relationship("ChildProfile", backref="parent", lazy=True)
    alerts = db.relationship("Alert", backref="parent", lazy=True)
    reports = db.relationship("SummaryReport", backref="parent", lazy=True)

    # ===============================
    # METHODS (MATCHING CLASS DIAGRAM)
    # ===============================

    # Update profile (Requirement 4)
    def updateProfile(self, email=None, passwordHash=None):
        if email:
            self.email = email
        if passwordHash:
            self.passwordHash = passwordHash
        db.session.commit()

    # Create Child Profile (Requirement 6)
    def createChildProfile(self, label, ageRange):
        from domain_models.child_model import ChildProfile

        child = ChildProfile(
            label=label,
            ageRange=ageRange,
            parentId=self.parentId
        )
        db.session.add(child)
        db.session.commit()
        return child

    # Edit Child Profile (Requirement 7)
    def editChildProfile(self, childId, label, ageRange):
        from domain_models.child_model import ChildProfile

        child = ChildProfile.query.get(childId)
        if child and child.parentId == self.parentId:
            child.updateLabels(label, ageRange)
            db.session.commit()
            return True
        return False

    # Enter Daily Activity (Requirement 13)
    def enterDailyActivity(self, childId, study, sleep, screen, spending):
        from domain_models.activity_model import DailyActivity

        activity = DailyActivity(
            studyTime=study,
            sleepDuration=sleep,
            screenTime=screen,
            spendingFrequency=spending,
            activityDate=datetime.utcnow(),
            childId=childId
        )
        db.session.add(activity)
        db.session.commit()
        return activity

    # View summaries (Requirement 14,15,20)
    def viewSummaries(self, start_date=None, end_date=None):
        from domain_models.report_model import SummaryReport

        query = SummaryReport.query.filter_by(parentId=self.parentId)

        if start_date and end_date:
            query = query.filter(
                SummaryReport.createdAt >= start_date,
                SummaryReport.createdAt <= end_date
            )

        return query.all()

    # Add observation note (Requirement 23)
    def addObservation(self, reportId, note):
        from domain_models.report_model import SummaryReport

        report = SummaryReport.query.get(reportId)
        if report and report.parentId == self.parentId:
            report.observationNote = note
            db.session.commit()
            return True
        return False