
import math
import unittest

from predictor import predict


class TestPropertyPredictor(unittest.TestCase):

    def setUp(self):
        self.sample_features = [
            3.5,    # Median income
            20.0,   # House age
            5.0,    # Average rooms
            1.0,    # Average bedrooms
            1000.0, # Population
            3.0,    # Average occupancy
            34.0,   # Latitude
            -120.0  # Longitude
        ]

    def test_prediction_is_numeric(self):
        result = predict(self.sample_features)
        self.assertIsInstance(result, (int, float))

    def test_prediction_is_finite(self):
        result = predict(self.sample_features)
        self.assertTrue(math.isfinite(result))

    def test_wrong_number_of_features_raises_error(self):
        with self.assertRaises(ValueError):
            predict([1.0, 2.0, 3.0])

    def test_prediction_in_expected_target_range(self):
        result = predict(self.sample_features)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 5.01)


if __name__ == "__main__":
    unittest.main()
