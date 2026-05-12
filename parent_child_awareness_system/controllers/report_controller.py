from flask import Blueprint, render_template, session, request, send_file
from business_logic.report_logic import ReportService
from business_logic.alert_logic import AlertService

import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

report_bp = Blueprint("report", __name__)


# -------------------------
# PDF GENERATION FUNCTION
# -------------------------
def generate_weekly_pdf(childId, report):

    os.makedirs("reports", exist_ok=True)

    file_path = f"reports/weekly_{childId}.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)

    c.setFont("Helvetica", 14)
    c.drawString(100, 750, "Weekly Routine Report")

    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Consistency Level: {report['level']}")
    c.drawString(100, 690, f"Explanation: {report['explanation']}")

    c.save()

    return file_path


# -------------------------
# DAILY REPORT
# -------------------------
@report_bp.route("/daily/<int:childId>")
def daily(childId):
    summary = ReportService.get_daily_summary(childId, None)
    return render_template("daily_summary_page.html", summary=summary)


# -------------------------
# WEEKLY REPORT
# -------------------------
@report_bp.route("/weekly/<int:childId>")
def weekly(childId):

    report = ReportService.generate_weekly_report(childId)

    # 🔥 Generate PDF automatically
    generate_weekly_pdf(childId, report)

    return render_template(
        "weekly_report_page.html",
        report=report,
        childId=childId
    )


# -------------------------
# DOWNLOAD PDF
# -------------------------
@report_bp.route("/download/weekly/<int:childId>")
def download_weekly(childId):

    file_path = f"reports/weekly_{childId}.pdf"

    if not os.path.exists(file_path):
        return "Report not found. Generate report first.", 404

    return send_file(file_path, as_attachment=True)


# -------------------------
# ALERTS
# -------------------------
@report_bp.route("/alerts")
def alerts():
    parentId = session["user_id"]
    alerts = AlertService.get_parent_alerts(parentId)
    return render_template("alerts_page.html", alerts=alerts)


# -------------------------
# FILTER REPORTS
# -------------------------
@report_bp.route("/filter", methods=["POST"])
def filter_reports():
    reports = ReportService.filter_reports(
        session["user_id"],
        request.form["start"],
        request.form["end"]
    )
    return render_template("weekly_report_page.html", reports=reports)