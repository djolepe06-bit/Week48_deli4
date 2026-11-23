"""Fraction exercises for INF201 Deliverable 4 task 2."""

from __future__ import annotations

from math import gcd


class Fraction:
    """Represent a rational number in lowest terms."""

    def __init__(self, numerator: int, denominator: int = 1):
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise TypeError("Numerator and denominator must be integers.")
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero.")

        if denominator < 0:
            numerator = -numerator
            denominator = -denominator

        divisor = gcd(abs(numerator), abs(denominator))
        self.numerator = numerator // divisor
        self.denominator = denominator // divisor

    def __str__(self) -> str:
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"

    def __repr__(self) -> str:
        return f"Fraction({self.numerator}, {self.denominator})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Fraction):
            return NotImplemented
        return self.numerator * other.denominator == other.numerator * self.denominator

    def __add__(self, other: "Fraction") -> "Fraction":
        if not isinstance(other, Fraction):
            return NotImplemented
        return Fraction(
            self.numerator * other.denominator + other.numerator * self.denominator,
            self.denominator * other.denominator,
        )

    def __sub__(self, other: "Fraction") -> "Fraction":
        if not isinstance(other, Fraction):
            return NotImplemented
        return Fraction(
            self.numerator * other.denominator - other.numerator * self.denominator,
            self.denominator * other.denominator,
        )

    def __mul__(self, other: "Fraction") -> "Fraction":
        if not isinstance(other, Fraction):
            return NotImplemented
        return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other: "Fraction") -> "Fraction":
        if not isinstance(other, Fraction):
            return NotImplemented
        if other.numerator == 0:
            raise ZeroDivisionError("Cannot divide by zero fractional value.")
        return Fraction(self.numerator * other.denominator, self.denominator * other.numerator)

    def __float__(self) -> float:
        return self.numerator / self.denominator

    def to_decimal(self) -> float:
        return float(self)


def demo() -> None:
    a = Fraction(1, 2)
    b = Fraction(3, 4)
    c = Fraction(-6, 8)

    print(f"a = {a}")
    print(f"b = {b}")
    print(f"c = {c}")
    print(f"a + b = {a + b}")
    print(f"a - b = {a - b}")
    print(f"a * b = {a * b}")
    print(f"a / b = {a / b}")
    print(f"Fraction(2,4) == Fraction(1,2): {Fraction(2, 4) == Fraction(1, 2)}")
    print(f"float(Fraction(3, 4)) = {float(Fraction(3, 4))}")


if __name__ == "__main__":
    demo()
