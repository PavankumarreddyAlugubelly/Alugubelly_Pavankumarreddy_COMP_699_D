from flask import Blueprint, render_template, request, redirect, url_for, session
from business_logic.auth_logic import AuthService

auth_bp = Blueprint("auth", __name__)


# ===============================
# LOGIN (PARENT + ADMIN)
# ===============================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # -------------------------------
        # TRY PARENT LOGIN
        # -------------------------------
        user, msg = AuthService.login_parent(email, password)

        if user:
            session.clear()
            session["user_id"] = user.parentId
            session["role"] = "parent"
            return redirect(url_for("parent.dashboard"))

        # -------------------------------
        # TRY ADMIN LOGIN
        # -------------------------------
        admin, msg_admin = AuthService.login_admin(email, password)

        if admin:
            session.clear()
            session["admin_id"] = admin.adminId
            session["role"] = "admin"
            return redirect(url_for("admin.admin_dashboard"))

        # -------------------------------
        # LOGIN FAILED
        # -------------------------------
        return render_template("login_page.html", error="Invalid email or password")

    return render_template("login_page.html")


# ===============================
# REGISTER (PARENT ONLY)
# ===============================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user, msg = AuthService.register_parent(
            request.form["email"],
            request.form["password"]
        )

        if user:
            return redirect(url_for("auth.login"))

        return render_template("register_page.html", error=msg)

    return render_template("register_page.html")


# ===============================
# LOGOUT
# ===============================
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


# ===============================
# OPTIONAL: SEPARATE ADMIN LOGIN (NOT REQUIRED NOW)
# ===============================
@auth_bp.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        admin, msg = AuthService.login_admin(
            request.form["username"],
            request.form["password"]
        )

        if admin:
            session.clear()
            session["admin_id"] = admin.adminId
            session["role"] = "admin"
            return redirect(url_for("admin.admin_dashboard"))

        return render_template("login_page.html", error=msg)

    return render_template("login_page.html")