from datetime import date
from typing import Optional, Tuple

WEIGHTS = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]

def _calc_control_digit(pesel: str) -> int:
    """
    Calculating the control digit 0-9 for a given PESEL.

    Args:
        pesel (str): pesel as a string of 11 digits (the last digit is calculated).
    Returns:
        int: Control digit(0-9).
    """
    s = sum(int(pesel[i]) * WEIGHTS[i] for i in range(10))
    return (10 - s % 10) % 10

def _decode_month_and_century(month_code: int) -> Tuple[Optional[int], Optional[int]]:
    """
    Decodes the encoded month from PESEL to century and real month.

    Args:
        month_code (int): Encoded month value from PESEL (2nd and 3rd digits).
    Returns:
        Tuple[Optional[int], Optional[int]]: 
            - (century, real_month) if the month_code is valid,
            - (None, None) if the month_code is invalid.
    """
    if 1 <= month_code <= 12:
        return 1900, month_code
    if 21 <= month_code <= 32:
        return 2000, month_code - 20
    if 41 <= month_code <= 52:
        return 2100, month_code - 40
    if 61 <= month_code <= 72:
        return 2200, month_code - 60
    if 81 <= month_code <= 92:
        return 1800, month_code - 80
    return None, None

def _parse_birth_date(year_two: int, month_code: int, day: int) -> Tuple[Optional[date], Optional[str]]:
    """
    Parses the encoded year, month, and day from PESEL into a datetime.date object.

    Args:
        year_two (int): Last two digits of the year from PESEL.
        month_code (int): Encoded month from PESEL.
        day (int): Day of birth from PESEL.
    Returns:
        Tuple[Optional[date], Optional[str]]:
            - (birth_date, None) if the date is valid,
            - (None, error_message) if the month_code or date is invalid.
    """
    century, month = _decode_month_and_century(month_code)
    if century is None:
        return None, "Nieprawidłowy miesiąc"

    full_year = century + year_two
    try:
        birth_date = date(full_year, month, day)
        return birth_date, None
    except ValueError:
        return None, "Nieprawidłowa data urodzenia"

def validate_pesel(pesel: str) -> dict:
    if not isinstance(pesel, str):
            return {"valid": False, "pesel": str(pesel), "error": "PESEL musi być łańcuchem znaków"}
    
    if not pesel.isdigit() or len(pesel) != 11:
        return {"valid": False, "pesel": pesel, "error": "PESEL musi składać się z 11 cyfr"}

    calc = _calc_control_digit(pesel)
    if calc != int(pesel[10]):
        return {"valid": False, "pesel": pesel, "error": "Nieprawidłowa cyfra kontrolna"}

    year = int(pesel[0:2])
    month_code = int(pesel[2:4])
    day = int(pesel[4:6])

    birth_date_obj, birth_error = _parse_birth_date(year, month_code, day)
    if birth_error:
        return {"valid": False, "pesel": pesel, "error": birth_error}
    
    print(birth_date_obj)  # debug
    return {"valid": True, "pesel": pesel, "error": None}