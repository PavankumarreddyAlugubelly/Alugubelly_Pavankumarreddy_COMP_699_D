from domain_models import db


class ChildProfile(db.Model):
    __tablename__ = "child_profiles"

    # ===============================
    # COLUMNS
    # ===============================
    childId = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    ageRange = db.Column(db.String(50), nullable=False)

    parentId = db.Column(db.Integer, db.ForeignKey("parents.parentId"), nullable=False)

    # ===============================
    # RELATIONSHIPS
    # ===============================

    # IMPORTANT: Use string names (avoids circular import issues)
    routines = db.relationship(
        "RoutinePlan",
        backref="child",
        lazy=True,
        cascade="all, delete-orphan"
    )

    activities = db.relationship(
        "DailyActivity",
        backref="child",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # ===============================
    # METHODS (CLASS DIAGRAM MATCH)
    # ===============================

    # Requirement 7 → Update child labels
    def updateLabels(self, label, ageRange):
        self.label = label
        self.ageRange = ageRange
        db.session.commit()

    # Requirement 8–11 → Create routine plan
    def createRoutinePlan(self, study, sleep, screen, spending):
        from domain_models.routine_model import RoutinePlan

        plan = RoutinePlan(
            studyTarget=study,
            sleepTarget=sleep,
            screenLimit=screen,
            spendingBand=spending,
            archived=False,
            childId=self.childId
        )

        db.session.add(plan)
        db.session.commit()

        return plan

    # Requirement → Get active routine
    def getActiveRoutine(self):
        from domain_models.routine_model import RoutinePlan

        return RoutinePlan.query.filter_by(
            childId=self.childId,
            archived=False
        ).first()

    # Optional → Get all activities
    def getActivities(self):
        from domain_models.activity_model import DailyActivity

        return DailyActivity.query.filter_by(childId=self.childId).all()

    # Optional → Delete child (safe cascade)
    def deleteProfile(self):
        db.session.delete(self)
        db.session.commit()

    # ===============================
    # STRING REPRESENTATION (DEBUG)
    # ===============================
    def __repr__(self):
        return f"<ChildProfile {self.label} ({self.ageRange})>"