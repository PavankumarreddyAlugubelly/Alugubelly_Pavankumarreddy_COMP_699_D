from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import ALL models so SQLAlchemy knows them
from domain_models.parent_model import Parent
from domain_models.child_model import ChildProfile
from domain_models.routine_model import RoutinePlan
from domain_models.activity_model import DailyActivity
from domain_models.alert_model import Alert
from domain_models.report_model import SummaryReport
from domain_models.admin_model import SystemAdmin