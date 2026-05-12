from datetime import datetime
from domain_models import db
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class SummaryReport(db.Model):
    __tablename__ = "summary_reports"

    reportId = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String(50))  # daily / weekly
    content = db.Column(db.Text)

    consistencyLevel = db.Column(db.String(50))
    explanation = db.Column(db.Text)

    observationNote = db.Column(db.Text)

    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    parentId = db.Column(db.Integer, db.ForeignKey("parents.parentId"), nullable=False)

    # ===============================
    # METHODS (MATCHING CLASS DIAGRAM)
    # ===============================

    # Generate daily summary (Requirement 14)
    @staticmethod
    def generateDaily(data, parentId, consistency, explanation):
        content = f"""
        Study: {data.studyTime} hrs
        Sleep: {data.sleepDuration} hrs
        Screen: {data.screenTime} hrs
        Spending: {data.spendingFrequency}
        """

        report = SummaryReport(
            type="DAILY",
            content=content,
            consistencyLevel=consistency,
            explanation=explanation,
            parentId=parentId
        )
        db.session.add(report)
        db.session.commit()
        return report

    # Generate weekly summary (Requirement 15)
    @staticmethod
    def generateWeekly(data_list, parentId, consistency, explanation):
        total_study = sum(d.studyTime for d in data_list)
        total_sleep = sum(d.sleepDuration for d in data_list)
        total_screen = sum(d.screenTime for d in data_list)
        total_spending = sum(d.spendingFrequency for d in data_list)

        content = f"""
        Weekly Totals:
        Study: {total_study}
        Sleep: {total_sleep}
        Screen: {total_screen}
        Spending: {total_spending}
        """

        report = SummaryReport(
            type="WEEKLY",
            content=content,
            consistencyLevel=consistency,
            explanation=explanation,
            parentId=parentId
        )
        db.session.add(report)
        db.session.commit()
        return report

    # Export PDF (Requirement 21)
    def exportPDF(self, file_path):
        doc = SimpleDocTemplate(file_path)
        styles = getSampleStyleSheet()

        elements = []

        elements.append(Paragraph(f"Report Type: {self.type}", styles["Title"]))
        elements.append(Paragraph(f"Content: {self.content}", styles["Normal"]))
        elements.append(Paragraph(f"Consistency: {self.consistencyLevel}", styles["Normal"]))
        elements.append(Paragraph(f"Explanation: {self.explanation}", styles["Normal"]))

        if self.observationNote:
            elements.append(Paragraph(f"Note: {self.observationNote}", styles["Normal"]))

        doc.build(elements)
        return file_path