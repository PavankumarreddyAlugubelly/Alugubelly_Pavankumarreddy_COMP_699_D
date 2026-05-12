from flask import Blueprint, render_template, request, session, redirect, url_for
from domain_models.admin_model import SystemAdmin

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        return redirect(url_for("auth.admin_login"))

    admin = SystemAdmin.query.get(session["admin_id"])
    users = admin.viewParentAccounts()

    return render_template("admin_dashboard_page.html", users=users)


# Activate user (Req 28)
@admin_bp.route("/activate/<int:id>")
def activate(id):
    admin = SystemAdmin.query.get(session["admin_id"])
    admin.activateParentAccount(id)
    return redirect(url_for("admin.admin_dashboard"))


# Deactivate user (Req 29)
@admin_bp.route("/deactivate/<int:id>")
def deactivate(id):
    admin = SystemAdmin.query.get(session["admin_id"])
    admin.deactivateParentAccount(id)
    return redirect(url_for("admin.admin_dashboard"))


# Category management (Req 30–33)
@admin_bp.route("/categories", methods=["GET", "POST"])
def categories():
    admin = SystemAdmin.query.get(session["admin_id"])

    if request.method == "POST":
        admin.createRoutineCategory(request.form["label"])

    categories = admin.viewRoutineCategories()
    return render_template("manage_categories_page.html", categories=categories)