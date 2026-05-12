from ml_engine.decision_engine import DecisionTreeEngine


class MLModel:

    def __init__(self):
        self.modelId = "DT-001"
        self.modelName = "DecisionTreeConsistencyModel"
        self.engine = DecisionTreeEngine()

    # MATCH CLASS DIAGRAM
    def analyzePatterns(self, data_list):
        deviations = []

        for data in data_list:
            if self.engine.detectBehaviorChanges(data):
                deviations.append(data)

        return deviations

    # MATCH CLASS DIAGRAM
    def computeConsistency(self, data_list):
        if not data_list:
            return "No Data", "No activity recorded."

        total_days = len(data_list)
        good_days = 0

        for data in data_list:
            if not self.engine.detectBehaviorChanges(data):
                good_days += 1

        score = good_days / total_days

        # Classification
        if score > 0.75:
            level = "GOOD"
            explanation = "Routine is consistent with minor deviations."
        elif score > 0.4:
            level = "MODERATE"
            explanation = "Some inconsistencies detected in routine."
        else:
            level = "POOR"
            explanation = "Frequent deviations detected in routine behavior."

        return level, explanation