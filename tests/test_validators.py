import unittest

from validators import valid_amount, valid_date, valid_month, valid_text


class ValidatorTests(unittest.TestCase):
    def test_valid_values_are_normalized(self):
        self.assertEqual(valid_amount("10.567"), 10.57)
        self.assertEqual(valid_date("2026-09-01"), "2026-09-01")
        self.assertEqual(valid_month("2026-09"), "2026-09")
        self.assertEqual(valid_text(" Lunch ", "Description"), "Lunch")

    def test_invalid_values_raise_value_error(self):
        for value in ("zero", "0", "-5"):
            with self.assertRaises(ValueError):
                valid_amount(value)
        with self.assertRaises(ValueError):
            valid_date("01-09-2026")
        with self.assertRaises(ValueError):
            valid_month("September")
        with self.assertRaises(ValueError):
            valid_text("", "Description")

