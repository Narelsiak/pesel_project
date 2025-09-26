from datetime import date
from typing import Optional, Tuple

WEIGHTS = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]

def _calc_control_digit(pesel: str) -> int:

    s = sum(int(pesel[i]) * WEIGHTS[i] for i in range(10))
    return (10 - s % 10) % 10

def validate_pesel(pesel: str) -> dict:
    if not isinstance(pesel, str):
            return {"valid": False, "pesel": str(pesel), "error": "PESEL musi być łańcuchem znaków"}
    
    if not pesel.isdigit() or len(pesel) != 11:
        return {"valid": False, "pesel": pesel, "error": "PESEL musi składać się z 11 cyfr"}

    calc = _calc_control_digit(pesel)
    if calc != int(pesel[10]):
        return {"valid": False, "pesel": pesel, "error": "Nieprawidłowa cyfra kontrolna"}

    return {"valid": True, "pesel": pesel, "error": None}