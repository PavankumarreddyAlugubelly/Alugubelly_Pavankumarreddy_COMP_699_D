from domain_models import db
from domain_models.activity_model import DailyActivity
from domain_models.child_model import ChildProfile
from domain_models.alert_model import Alert
from domain_models.report_model import SummaryReport

from ml_engine.consistency_model import MLModel


class ActivityService:

    # Add Daily Activity
    @staticmethod
    def add_activity(childId, study, sleep, screen, spending):

        activity = DailyActivity(
            studyTime=study,
            sleepDuration=sleep,
            screenTime=screen,
            spendingFrequency=spending,
            childId=childId
        )

        if not activity.validate():
            return None, "Invalid activity data"

        db.session.add(activity)
        db.session.commit()

        # Run ML processing
        ActivityService.process_activity(activity)

        return activity, "Activity recorded"

    # MAIN FIX HERE
    @staticmethod
    def process_activity(activity):

        child = ChildProfile.query.get(activity.childId)
        parentId = child.parentId

        ml = MLModel()

        # ✅ NEW ANALYSIS METHOD
        analysis = ml.engine.analyzeBehavior(activity)

        # Consistency (existing)
        level, explanation = ml.computeConsistency([activity])

        # Save report
        SummaryReport.generateDaily(activity, parentId, level, explanation)

        # HANDLE ALERTS PROPERLY
        if analysis["type"] != "normal":

            if analysis["type"] == "negative":
                alert_level = "HIGH"
            else:
                alert_level = "POSITIVE"

            Alert.createAlert(
                parentId,
                analysis["message"],
                alert_level
            )

    # Get activities
    @staticmethod
    def get_child_activities(childId):
        return DailyActivity.query.filter_by(childId=childId).all()