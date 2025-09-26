"""
Tests for PESEL validation utils and view.

What`s tested:
- Utils: calculate control digit, decode month/century, parse birth date, extract gender, validate PESEL.
- View: pesel_view form (GET/POST, error messages).

Includes unit tests for functions and integration tests for the view.
"""

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

class PeselValidationTests(SimpleTestCase):
    """
    Higher-level unit tests for the validate_pesel function.
    Focuses on overall validation logic for correct and incorrect PESELs.
    """
    def test_valid_pesel(self) -> None:
        """Check that a valid PESEL returns the correct birth date, gender, and valid=True."""
        result: Dict = validate_pesel("44051401359")
        self.assertTrue(result['valid'])
        self.assertEqual(result['birth_date'], "1944-05-14")
        self.assertEqual(result['gender'], "Mężczyzna")

    def test_invalid_pesel_length(self) -> None:
        """Check that a PESEL with incorrect length is invalid and contains an error message."""
        result: Dict = validate_pesel("123")
        self.assertFalse(result['valid'])
        self.assertIn('error', result)

    def test_invalid_pesel_checksum(self) -> None:
        """Check that a PESEL with wrong checksum is invalid and contains an error message."""
        result: Dict = validate_pesel("44051401350")
        self.assertFalse(result['valid'])
        self.assertIn('error', result)

class PeselViewTests(TestCase):
    """
    Integration tests for the PESEL Django form view (pesel_view).
    Tests GET and POST requests, form rendering, redirection, and error message display.
    """
    def test_get_form(self) -> None:
        """GET request to the PESEL form should return 200 and contain the form title."""
        response = self.client.get(reverse('pesel_view'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Walidator PESEL")

    def test_post_valid_pesel(self) -> None:
        """POST a valid PESEL should redirect (POST-Redirect-GET) and return 200."""
        response = self.client.post(reverse('pesel_view'), {"pesel": "44051401359"}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_invalid_pesel(self) -> None:
        """POST an invalid PESEL should return 200 and show an error message."""
        response = self.client.post(reverse('pesel_view'), {"pesel": "12345678901"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Niepoprawny")
        self.assertContains(response, "Nieprawidłowa cyfra kontrolna")
