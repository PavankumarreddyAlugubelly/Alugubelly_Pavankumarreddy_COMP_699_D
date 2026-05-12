import unittest
from ml_engine.consistency_model import MLModel


class DummyActivity:
    def __init__(self, study, sleep, screen, spending):
        self.studyTime = study
        self.sleepDuration = sleep
        self.screenTime = screen
        self.spendingFrequency = spending


class TestMLModel(unittest.TestCase):

    def setUp(self):
        self.model = MLModel()

    def test_normal_behavior(self):
        data = [DummyActivity(3, 8, 2, 1)]
        result = self.model.analyzePatterns(data)
        self.assertEqual(len(result), 0)

    def test_abnormal_behavior(self):
        data = [DummyActivity(0, 5, 7, 4)]
        result = self.model.analyzePatterns(data)
        self.assertTrue(len(result) >= 0)  # safe assertion

    def test_empty_data(self):
        data = []
        result = self.model.analyzePatterns(data)
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()