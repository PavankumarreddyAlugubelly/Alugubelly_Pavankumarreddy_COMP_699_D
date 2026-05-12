from flask import Blueprint, render_template, request, session, redirect, url_for
from business_logic.activity_logic import ActivityService

activity_bp = Blueprint("activity", __name__)


@activity_bp.route("/add/<int:childId>", methods=["GET", "POST"])
def add_activity(childId):
    if request.method == "POST":
        ActivityService.add_activity(
            childId,
            int(request.form["study"]),
            int(request.form["sleep"]),
            int(request.form["screen"]),
            int(request.form["spending"])
        )
        return redirect(url_for("parent.dashboard"))

    return render_template("activity_entry_page.html", childId=childId)