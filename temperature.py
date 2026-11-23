"""Temperature class supporting Celsius, Fahrenheit and Kelvin."""

import math

TOLERANCE = 1e-9
_VALID_UNITS = ("C", "F", "K")


class Temperature:
    """A temperature in Celsius, Fahrenheit or Kelvin."""

    def __init__(self, value, unit="C"):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(
                f"value must be a number, got {type(value).__name__}"
            )
        if math.isnan(value):
            raise ValueError("value must not be NaN")
        if not isinstance(unit, str) or unit.upper() not in _VALID_UNITS:
            raise ValueError(
                f"unit must be one of 'C', 'F' or 'K', got {unit!r}"
            )

        unit = unit.upper()
        kelvin = self._to_kelvin_static(value, unit)
        if kelvin < -TOLERANCE:
            raise ValueError(
                f"temperature {value} {unit} is below absolute zero (0 K)"
            )

        self._value = float(value)
        self._unit = unit

    @property
    def value(self) -> float:
        return self._value

    @property
    def unit(self) -> str:
        return self._unit

    @staticmethod
    def _to_kelvin_static(value, unit):
        if unit == "K":
            return value
        if unit == "C":
            return value + 273.15
        return (value - 32) * 5 / 9 + 273.15

    def to_celsius(self) -> float:
        if self._unit == "C":
            return self._value
        if self._unit == "K":
            return self._value - 273.15
        return (self._value - 32) * 5 / 9

    def to_fahrenheit(self) -> float:
        if self._unit == "F":
            return self._value
        if self._unit == "C":
            return self._value * 9 / 5 + 32
        return (self._value - 273.15) * 9 / 5 + 32

    def to_kelvin(self) -> float:
        if self._unit == "K":
            return self._value
        if self._unit == "C":
            return self._value + 273.15
        return (self._value - 32) * 5 / 9 + 273.15

    def convert_to(self, target_unit: str) -> "Temperature":
        if not isinstance(target_unit, str) or target_unit.upper() not in _VALID_UNITS:
            raise ValueError(
                f"target_unit must be one of 'C', 'F' or 'K', got {target_unit!r}"
            )

        target = target_unit.upper()
        if target == "C":
            return Temperature(self.to_celsius(), "C")
        if target == "F":
            return Temperature(self.to_fahrenheit(), "F")
        return Temperature(self.to_kelvin(), "K")

    def __repr__(self) -> str:
        return f"Temperature({self._value!r}, {self._unit!r})"

    def __str__(self) -> str:
        if self._unit == "K":
            return f"{self._value:.2f} K"
        return f"{self._value:.2f} °{self._unit}"

    def _is_close(self, other: "Temperature") -> bool:
        return abs(self.to_kelvin() - other.to_kelvin()) <= TOLERANCE

    def __eq__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._is_close(other)

    def __ne__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return not self._is_close(other)

    def __lt__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return not self._is_close(other) and self.to_kelvin() < other.to_kelvin()

    def __le__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._is_close(other) or self.to_kelvin() < other.to_kelvin()

    def __gt__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return not self._is_close(other) and self.to_kelvin() > other.to_kelvin()

    def __ge__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._is_close(other) or self.to_kelvin() > other.to_kelvin()

    __hash__ = None
