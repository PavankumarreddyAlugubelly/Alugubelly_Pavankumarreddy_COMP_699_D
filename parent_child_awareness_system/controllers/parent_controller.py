from flask import Blueprint, render_template, request, session, redirect, url_for
from domain_models.parent_model import Parent

parent_bp = Blueprint("parent", __name__)


@parent_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    parent = Parent.query.get(session["user_id"])
    children = parent.children

    return render_template("dashboard_page.html", parent=parent, children=children)


# Create child (Req 6)
@parent_bp.route("/add_child", methods=["POST"])
def add_child():
    parent = Parent.query.get(session["user_id"])
    parent.createChildProfile(
        request.form["label"],
        request.form["age"]
    )
    return redirect(url_for("parent.dashboard"))


# Edit child (Req 7)
@parent_bp.route("/edit_child/<int:childId>", methods=["POST"])
def edit_child(childId):
    parent = Parent.query.get(session["user_id"])
    parent.editChildProfile(
        childId,
        request.form["label"],
        request.form["age"]
    )
    return redirect(url_for("parent.dashboard"))