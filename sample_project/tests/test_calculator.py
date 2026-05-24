import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from sample_project.calculator import add, subtract, multiply, divide, power, is_even
import pytest

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(10, 4) == 6
    assert subtract(0, 5) == -5

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(0, 100) == 0

def test_divide():
    assert divide(10, 2) == 5.0
    assert divide(7, 2) == 3.5

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(5, 0)

def test_power():
    assert power(2, 3) == 8
    assert power(5, 0) == 1

def test_is_even():
    assert is_even(4) == True
    assert is_even(7) == False


# ── AI Generated Tests (Phase 2) ──────────────────────
def test_add_negative_numbers():
    assert add(-2, -3) == -5
    assert add(-1, -1) == -2

def test_add_large_numbers():
    assert add(1000000, 2000000) == 3000000

def test_subtract_negative_numbers():
    assert subtract(-1, -2) == 1
    assert subtract(-5, 0) == -5

def test_subtract_large_numbers():
    assert subtract(2000000, 1000000) == 1000000

def test_multiply_negative_numbers():
    assert multiply(-1, -2) == 2
    assert multiply(-1, 2) == -2

def test_multiply_large_numbers():
    assert multiply(1000000, 2000000) == 2000000000000

def test_divide_negative_numbers():
    assert divide(-1, 2) == -0.5
    assert divide(1, -2) == -0.5

def test_divide_large_numbers():
    assert divide(2000000, 1000000) == 2.0

def test_power_negative_exponent():
    assert power(2, -1) == 0.5
    assert power(2, -2) == 0.25

def test_power_non_integer_exponent():
    assert power(2, 0.5) == 1.4142135623730951

def test_is_even_zero():
    assert is_even(0) == True

def test_is_even_negative():
    assert is_even(-4) == True
    assert is_even(-7) == False

def test_add_type_error():
    with pytest.raises(TypeError):
        add(2, 'a')

def test_subtract_type_error():
    with pytest.raises(TypeError):
        subtract(2, 'a')

def test_multiply_type_error():
    # Python allows multiply with string (repeats it), so test actual behavior
    assert multiply(3, "a") == "aaa"

def test_divide_type_error():
    with pytest.raises(TypeError):
        divide(2, 'a')

def test_power_type_error():
    with pytest.raises(TypeError):
        power(2, 'a')

def test_is_even_type_error():
    with pytest.raises(TypeError):
        is_even('a')