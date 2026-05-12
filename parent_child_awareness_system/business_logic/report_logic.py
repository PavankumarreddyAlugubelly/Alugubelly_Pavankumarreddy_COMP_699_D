from datetime import datetime, timedelta
from domain_models.activity_model import DailyActivity
from domain_models.report_model import SummaryReport
from domain_models.child_model import ChildProfile

from ml_engine.consistency_model import MLModel


class ReportService:

    # Daily summary (Req 14)
    @staticmethod
    def get_daily_summary(childId, date):
        activity = DailyActivity.query.filter_by(
            childId=childId
        ).order_by(DailyActivity.activityDate.desc()).first()

        return activity

    # Weekly report (Req 15)
    @staticmethod
    def generate_weekly_report(childId):
        last_week = datetime.utcnow() - timedelta(days=7)

        activities = DailyActivity.query.filter(
            DailyActivity.childId == childId,
            DailyActivity.activityDate >= last_week
        ).all()

        if not activities:
            return None

        child = ChildProfile.query.get(childId)
        parentId = child.parentId

        ml = MLModel()
        level, explanation = ml.computeConsistency(activities)

        return SummaryReport.generateWeekly(
            activities,
            parentId,
            level,
            explanation
        )

    # Filter reports (Req 20)
    @staticmethod
    def filter_reports(parentId, start, end):
        return SummaryReport.query.filter(
            SummaryReport.parentId == parentId,
            SummaryReport.createdAt >= start,
            SummaryReport.createdAt <= end
        ).all()

    # Download PDF (Req 21)
    @staticmethod
    def export_report(reportId, path):
        report = SummaryReport.query.get(reportId)
        if report:
            return report.exportPDF(path)
        return None