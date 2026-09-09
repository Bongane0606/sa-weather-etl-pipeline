import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from transform import transform_city_weather, transform_all
from validate import validate_city, validate_all
def make_raw_city(name="Johannesburg", province="Gauteng", temp=18.5, humidity=65, wind=3.5):
    """Helper that builds a fake raw API response."""
    return {
        "name": name,
        "province": province,
        "sys": {"country": "ZA"},
        "main": {
            "temp": temp,
            "feels_like": temp - 1.5,
            "temp_min": temp - 3.0,
            "temp_max": temp + 2.5,
            "humidity": humidity
        },
        "wind": {"speed": wind},
        "weather": [{"description": "clear sky"}]
    }


def make_transformed_city(
    city="Johannesburg", province="Gauteng", temp=18.5, humidity=65,
    wind=3.5, temp_min=15.0, temp_max=21.0
):
    """Helper that builds a fake already-transformed city dict."""
    return {
        "city": city,
        "province": province,
        "country": "ZA",
        "temperature_c": temp,
        "feels_like_c": temp - 1.5,
        "temp_min_c": temp_min,
        "temp_max_c": temp_max,
        "humidity_percent": humidity,
        "wind_speed_mps": wind,
        "condition": "clear sky",
        "extracted_at": "2026-08-03 09:00:00"
    }


class TestTransform(unittest.TestCase):

    def test_transform_returns_correct_city_name(self):
        """Transformed data should have the correct city name."""
        raw = make_raw_city(name="Durban")
        result = transform_city_weather(raw)
        self.assertEqual(result["city"], "Durban")

    def test_transform_returns_correct_temperature(self):
        """Transformed data should carry the correct temperature."""
        raw = make_raw_city(temp=22.0)
        result = transform_city_weather(raw)
        self.assertEqual(result["temperature_c"], 22.0)

    def test_transform_contains_all_required_fields(self):
        """Transformed data must contain all expected fields."""
        raw = make_raw_city()
        result = transform_city_weather(raw)
        expected_fields = [
            "city", "province", "country", "temperature_c", "feels_like_c",
            "temp_min_c", "temp_max_c", "humidity_percent",
            "wind_speed_mps", "condition", "extracted_at"
        ]
        for field in expected_fields:
            self.assertIn(field, result)

    def test_transform_all_returns_correct_count(self):
        """transform_all should return same number of cities as input."""
        raw_list = [make_raw_city("Joburg"), make_raw_city("Cape Town")]
        result = transform_all(raw_list)
        self.assertEqual(len(result), 2)

    def test_transform_extracted_at_is_not_empty(self):
        """extracted_at timestamp should never be empty."""
        raw = make_raw_city()
        result = transform_city_weather(raw)
        self.assertTrue(len(result["extracted_at"]) > 0)


class TestValidate(unittest.TestCase):

    def test_valid_city_passes(self):
        """A clean, realistic city record should pass validation."""
        city = make_transformed_city()
        self.assertTrue(validate_city(city))

    def test_missing_city_name_fails(self):
        """A record with an empty city name should fail validation."""
        city = make_transformed_city()
        city["city"] = ""
        self.assertFalse(validate_city(city))

    def test_temperature_too_high_fails(self):
        """A temperature above 60°C should fail validation."""
        city = make_transformed_city(temp=99.0, temp_min=97.0, temp_max=101.0)
        self.assertFalse(validate_city(city))

    def test_temperature_too_low_fails(self):
        """A temperature below -20°C should fail validation."""
        city = make_transformed_city(temp=-50.0, temp_min=-55.0, temp_max=-45.0)
        self.assertFalse(validate_city(city))

    def test_humidity_over_100_fails(self):
        """Humidity above 100% is physically impossible — should fail."""
        city = make_transformed_city(humidity=150)
        self.assertFalse(validate_city(city))

    def test_humidity_negative_fails(self):
        """Negative humidity should fail validation."""
        city = make_transformed_city(humidity=-10)
        self.assertFalse(validate_city(city))

    def test_temp_min_greater_than_temp_max_fails(self):
        """temp_min should never be greater than temp_max."""
        city = make_transformed_city(temp_min=25.0, temp_max=10.0)
        self.assertFalse(validate_city(city))

    def test_validate_all_filters_bad_records(self):
        """validate_all should remove failing cities and keep passing ones."""
        good_city = make_transformed_city("Durban")
        bad_city = make_transformed_city("FakeCity", humidity=999)
        result = validate_all([good_city, bad_city])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["city"], "Durban")

    def test_validate_all_empty_input(self):
        """validate_all with empty input should return empty list."""
        result = validate_all([])
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)