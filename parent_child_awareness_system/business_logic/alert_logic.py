from domain_models.alert_model import Alert


class AlertService:

    # Get alerts (Req 16,17)
    @staticmethod
    def get_parent_alerts(parentId):
        return Alert.query.filter_by(parentId=parentId).order_by(Alert.createdAt.desc()).all()

    # Count alerts (useful for dashboard)
    @staticmethod
    def count_alerts(parentId):
        return Alert.query.filter_by(parentId=parentId).count()

    # Manual alert (admin use)
    @staticmethod
    def create_custom_alert(parentId, message, severity="MEDIUM"):
        return Alert.createAlert(parentId, message, severity)