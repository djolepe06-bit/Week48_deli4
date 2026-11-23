
import pytest


class Fraction:
    """A fraction numerator/denominator with integer parts and denominator > 0."""

    def __init__(self, numerator: int, denominator: int = 1):
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise TypeError("numerator and denominator must be integers")
        if denominator <= 0:
            raise ValueError("denominator must be strictly positive")
        self.numerator = numerator
        self.denominator = denominator

    # ------------------------------------------------
    # all comparisons
    def __eq__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return self.numerator * other.denominator == other.numerator * self.denominator

    def __ne__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return self.numerator * other.denominator != other.numerator * self.denominator

    def __lt__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return self.numerator * other.denominator < other.numerator * self.denominator

    def __le__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return self.numerator * other.denominator <= other.numerator * self.denominator

    def __gt__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return self.numerator * other.denominator > other.numerator * self.denominator

    # ----------------------------------------------------------------------------------
    # Special methods

    def __ge__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return self.numerator * other.denominator >= other.numerator * self.denominator

    def __add__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented 
        num = self.numerator * other.denominator + other.numerator * self.denominator
        den = self.denominator * other.denominator
        return Fraction(num, den)

    def __sub__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        num = self.numerator * other.denominator - other.numerator * self.denominator
        den = self.denominator * other.denominator
        return Fraction(num, den)

    def __mul__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return Fraction(self.numerator * other.numerator,
                        self.denominator * other.denominator)

    def __truediv__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        if other.numerator == 0:
            raise ZeroDivisionError("cannot divide by a zero fraction")
        num = self.numerator * other.denominator
        den = self.denominator * other.numerator
        if den < 0:              # keep the denominator positive
            num, den = -num, -den
        return Fraction(num, den)


def test_default_denominator():
    f = Fraction(3)
    assert f.numerator == 3
    assert f.denominator == 1


def test_rejects_invalid_values():
    with pytest.raises(TypeError):
        Fraction(1.5, 2)
    with pytest.raises(ValueError):
        Fraction(1, 0)
    with pytest.raises(ValueError):
        Fraction(1, -2)


def test_arithmetic():
    a = Fraction(1, 2)
    b = Fraction(1, 3)
    assert a + b == Fraction(5, 6)
    assert a - b == Fraction(1, 6)
    assert a * b == Fraction(1, 6)
    assert a / b == Fraction(3, 2)


def test_comparisons():
    a = Fraction(1, 2)
    b = Fraction(2, 3)
    assert a != b
    assert a < b
    assert a <= b
    assert b > a
    assert b >= a


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        Fraction(1, 2) / Fraction(0)
