from typing import Dict
from datetime import date
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
import peselapp.utils as utils
from peselapp.utils import validate_pesel

class TestPeselUtils(SimpleTestCase):
    """
    Unit tests for the internal PESEL utility functions.
    """

    def test_calc_control_digit(self) -> None:
        """Check that the control digit is calculated correctly for given PESEL prefixes."""
        self.assertEqual(utils._calc_control_digit("4405140135"), 9)
        self.assertEqual(utils._calc_control_digit("1234567890"), 3)

    def test_decode_month_and_century(self) -> None:
        """Check that month codes are decoded to correct century and real month."""
        self.assertEqual(utils._decode_month_and_century(5), (1900, 5))
        self.assertEqual(utils._decode_month_and_century(25), (2000, 5))
        self.assertEqual(utils._decode_month_and_century(45), (2100, 5))
        self.assertEqual(utils._decode_month_and_century(65), (2200, 5))
        self.assertEqual(utils._decode_month_and_century(85), (1800, 5))
        self.assertEqual(utils._decode_month_and_century(13), (None, None))  # invalid month

    def test_parse_birth_date(self) -> None:
        """Check that birth date parsing works and invalid dates return appropriate errors."""
        d, err = utils._parse_birth_date(44, 5, 14)
        self.assertEqual(d, date(1944, 5, 14))
        self.assertIsNone(err)

        d, err = utils._parse_birth_date(44, 15, 14)
        self.assertIsNone(d)
        self.assertEqual(err, "Nieprawidłowy miesiąc")

        d, err = utils._parse_birth_date(44, 2, 31)
        self.assertIsNone(d)
        self.assertEqual(err, "Nieprawidłowa data urodzenia")

    def test_extract_gender(self) -> None:
        """Check that the gender extraction from PESEL works correctly."""
        self.assertEqual(utils._extract_gender("44051401359"), "Mężczyzna")
        self.assertEqual(utils._extract_gender("44051401368"), "Kobieta")

    def test_validate_pesel(self) -> None:
        """Check validate_pesel for valid and invalid PESELs."""
        result = validate_pesel("44051401359")
        self.assertTrue(result["valid"])
        self.assertEqual(result["birth_date"], "1944-05-14")
        self.assertEqual(result["gender"], "Mężczyzna")

        result = validate_pesel("123")
        self.assertFalse(result["valid"])
        self.assertIn("error", result)

        result = validate_pesel("44051401350")
        self.assertFalse(result["valid"])
        self.assertIn("error", result)