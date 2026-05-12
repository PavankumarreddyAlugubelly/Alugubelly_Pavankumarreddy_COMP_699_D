from domain_models import db
from datetime import datetime


class RoutinePlan(db.Model):
    __tablename__ = "routine_plans"

    # ===============================
    # COLUMNS
    # ===============================
    planId = db.Column(db.Integer, primary_key=True)

    studyTarget = db.Column(db.Integer, nullable=False)
    sleepTarget = db.Column(db.Integer, nullable=False)
    screenLimit = db.Column(db.Integer, nullable=False)
    spendingBand = db.Column(db.String(50), nullable=False)

    archived = db.Column(db.Boolean, default=False)

    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, onupdate=datetime.utcnow)

    childId = db.Column(
        db.Integer,
        db.ForeignKey("child_profiles.childId"),
        nullable=False
    )

    # ===============================
    # METHODS (CLASS DIAGRAM MATCH)
    # ===============================

    # Requirement 8–11 → Define targets
    def defineTargets(self, study, sleep, screen, spending):
        self.studyTarget = study
        self.sleepTarget = sleep
        self.screenLimit = screen
        self.spendingBand = spending
        db.session.commit()

    # Requirement 12 → Update targets
    def updateTargets(self, study, sleep, screen, spending):
        self.studyTarget = study
        self.sleepTarget = sleep
        self.screenLimit = screen
        self.spendingBand = spending
        db.session.commit()

    # Requirement 24 → Archive plan
    def archivePlan(self):
        self.archived = True
        db.session.commit()

    # Requirement 25 → Restore plan
    def restorePlan(self):
        self.archived = False
        db.session.commit()

    # ===============================
    # ADDITIONAL PROFESSIONAL METHODS
    # ===============================

    # Check if plan is active
    def isActive(self):
        return not self.archived

    # Get readable summary
    def getSummary(self):
        return {
            "study": self.studyTarget,
            "sleep": self.sleepTarget,
            "screen": self.screenLimit,
            "spending": self.spendingBand,
            "status": "Active" if not self.archived else "Archived"
        }

    # Soft update (without commit)
    def updateWithoutCommit(self, study, sleep, screen, spending):
        self.studyTarget = study
        self.sleepTarget = sleep
        self.screenLimit = screen
        self.spendingBand = spending

    # ===============================
    # STRING REPRESENTATION
    # ===============================
    def __repr__(self):
        return f"<RoutinePlan Child={self.childId} Study={self.studyTarget} Sleep={self.sleepTarget}>"