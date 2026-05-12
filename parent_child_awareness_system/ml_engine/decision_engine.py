from sklearn.tree import DecisionTreeClassifier


class DecisionTreeEngine:

    def __init__(self):
        self.treeDepth = 4
        self.trainedOn = "enhanced_behavior_data"

        self.model = DecisionTreeClassifier(max_depth=self.treeDepth)

        # Training Data
        # [study, sleep, screen, spending]

        X = [
            # ✅ GOOD behavior
            [4, 8, 2, 1],
            [5, 7, 1, 0],
            [3, 8, 2, 1],

            # ⚖️ MODERATE behavior
            [2, 6, 4, 3],
            [1, 6, 5, 3],

            # ❌ POOR / UNUSUAL behavior
            [0, 4, 6, 5],
            [0, 3, 7, 5],
            [1, 4, 6, 4]
        ]

        # Labels:
        # 0 = Good
        # 1 = Moderate
        # 2 = Poor (Unusual)
        y = [0, 0, 0, 1, 1, 2, 2, 2]

        self.model.fit(X, y)

    # ✅ MAIN METHOD (NEW LOGIC)
    def analyzeBehavior(self, data):

        features = [
            data.studyTime,
            data.sleepDuration,
            data.screenTime,
            data.spendingFrequency
        ]

        result = self.model.predict([features])[0]

        print("ML Prediction:", result, "Features:", features)

        # 🚨 NEGATIVE ALERT
        if result == 2:
            return {
                "type": "negative",
                "message": "Unusual behavior detected in routine"
            }

        # 🌟 POSITIVE ALERT (GOOD HABIT DETECTION)
        if data.studyTime >= 4 and data.screenTime == 0:
            return {
                "type": "positive",
                "message": "Excellent routine maintained"
            }

        # ✅ NORMAL CASE
        return {
            "type": "normal",
            "message": "Routine is consistent"
        }

    # ✅ BACKWARD COMPATIBILITY (IMPORTANT FIX FOR YOUR ERROR)
    def detectBehaviorChanges(self, data):
        analysis = self.analyzeBehavior(data)

        # Only negative triggers TRUE (for old code)
        return analysis["type"] == "negative"

    # ✅ OPTIONAL (FOR UI DISPLAY)
    def getConsistencyLevel(self, data):

        features = [
            data.studyTime,
            data.sleepDuration,
            data.screenTime,
            data.spendingFrequency
        ]

        result = self.model.predict([features])[0]

        if result == 0:
            return "High"
        elif result == 1:
            return "Medium"
        else:
            return "Low"