from flask import Flask, redirect, url_for
from settings import Config
from domain_models import db

# Controllers (Blueprints)
from controllers.auth_controller import auth_bp
from controllers.parent_controller import parent_bp
from controllers.activity_controller import activity_bp
from controllers.report_controller import report_bp
from controllers.admin_controller import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ================= DATABASE INIT =================
    db.init_app(app)

    # ================= REGISTER BLUEPRINTS =================
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(parent_bp, url_prefix="/parent")
    app.register_blueprint(activity_bp, url_prefix="/activity")
    app.register_blueprint(report_bp, url_prefix="/report")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # ================= HOME ROUTE =================
    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    # ================= CREATE DATABASE TABLES =================
    with app.app_context():
        db.create_all()

    return app


# ================= RUN APPLICATION =================
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="127.0.0.1", port=5000)