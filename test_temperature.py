import importlib.util
from pathlib import Path

import pytest

_temperature_path = Path(__file__).with_name("temperature.py")
_temperature_spec = importlib.util.spec_from_file_location("temperature", _temperature_path)
if _temperature_spec is None or _temperature_spec.loader is None:
    raise ImportError(f"Cannot load temperature module from {_temperature_path}")
_temperature_module = importlib.util.module_from_spec(_temperature_spec)
_temperature_spec.loader.exec_module(_temperature_module)
Temperature = _temperature_module.Temperature

# Reference points: (Celsius, Fahrenheit, Kelvin)
REFERENCE_POINTS = [
    pytest.param(-273.15, -459.67, 0.0, id="absolute-zero"),
    pytest.param(-40.0, -40.0, 233.15, id="c-f-crossover"),
    pytest.param(0.0, 32.0, 273.15, id="freezing-water"),
    pytest.param(37.0, 98.6, 310.15, id="body-temperature"),
    pytest.param(100.0, 212.0, 373.15, id="boiling-water"),
]


# ----------------------------------------------------------------------
# 1. Initialisation
# ----------------------------------------------------------------------
class TestInitialization:
    def test_default_unit_is_celsius(self):
        t = Temperature(25)
        assert t.unit == "C"
        assert t.value == 25.0

    def test_value_is_stored_as_float(self):
        assert isinstance(Temperature(25, "C").value, float)

    @pytest.mark.parametrize("unit", ["c", "C", "f", "F", "k", "K"])
    def test_case_insensitive_units(self, unit):
        assert Temperature(300, unit).unit == unit.upper()

    def test_value_is_read_only(self):
        t = Temperature(25, "C")
        with pytest.raises(AttributeError):
            t.value = 30

    def test_unit_is_read_only(self):
        t = Temperature(25, "C")
        with pytest.raises(AttributeError):
            t.unit = "F"


# ----------------------------------------------------------------------
# 2. Validation
# ----------------------------------------------------------------------
class TestValidation:
    @pytest.mark.parametrize("unit", ["X", "", "Celsius", "KK", " C"])
    def test_invalid_unit_string(self, unit):
        with pytest.raises(ValueError):
            Temperature(10, unit)

    def test_non_string_unit(self):
        with pytest.raises(ValueError):
            Temperature(10, 5)

    @pytest.mark.parametrize(
        "value, unit",
        [(-273.16, "C"), (-459.68, "F"), (-0.01, "K"), (-1000, "C")],
    )
    def test_below_absolute_zero(self, value, unit):
        with pytest.raises(ValueError):
            Temperature(value, unit)

    @pytest.mark.parametrize(
        "value, unit", [(-273.15, "C"), (-459.67, "F"), (0, "K")]
    )
    def test_absolute_zero_is_allowed(self, value, unit):
        Temperature(value, unit)  # must not raise


# ----------------------------------------------------------------------
# 3. Conversions
# ----------------------------------------------------------------------
class TestConversions:
    @pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
    def test_from_celsius(self, c, f, k):
        t = Temperature(c, "C")
        assert t.to_celsius() == pytest.approx(c)
        assert t.to_fahrenheit() == pytest.approx(f)
        assert t.to_kelvin() == pytest.approx(k)

    @pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
    def test_from_fahrenheit(self, c, f, k):
        t = Temperature(f, "F")
        assert t.to_celsius() == pytest.approx(c)
        assert t.to_fahrenheit() == pytest.approx(f)
        assert t.to_kelvin() == pytest.approx(k)

    @pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
    def test_from_kelvin(self, c, f, k):
        t = Temperature(k, "K")
        assert t.to_celsius() == pytest.approx(c)
        assert t.to_fahrenheit() == pytest.approx(f)
        assert t.to_kelvin() == pytest.approx(k)

    @pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
    def test_convert_to_returns_new_temperature(self, c, f, k):
        t = Temperature(c, "C")
        as_f = t.convert_to("F")
        as_k = t.convert_to("k")  # case-insensitive
        assert isinstance(as_f, Temperature)
        assert as_f.unit == "F" and as_f.value == pytest.approx(f)
        assert as_k.unit == "K" and as_k.value == pytest.approx(k)
        assert t.unit == "C" and t.value == c  # original unchanged

    def test_convert_to_invalid_unit(self):
        with pytest.raises(ValueError):
            Temperature(0, "C").convert_to("X")

    def test_convert_to_same_unit(self):
        t = Temperature(20, "C").convert_to("C")
        assert t.unit == "C" and t.value == 20.0


# ----------------------------------------------------------------------
# 4. Round-trip conversions
# ----------------------------------------------------------------------
class TestRoundTrip:
    @pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
    def test_c_f_k_c(self, c, f, k):
        original = Temperature(c, "C")
        back = original.convert_to("F").convert_to("K").convert_to("C")
        assert back.unit == "C"
        assert back.value == pytest.approx(c, abs=1e-9)
        assert back == original

    @pytest.mark.parametrize("value", [-100.0, 0.0, 21.5, 1234.5678])
    def test_round_trip_arbitrary_values(self, value):
        original = Temperature(value, "C")
        back = original.convert_to("F").convert_to("K").convert_to("C")
        assert back == original


# ----------------------------------------------------------------------
# 5. Cross-unit comparisons
# ----------------------------------------------------------------------
class TestComparisons:
    @pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
    def test_equality_across_units(self, c, f, k):
        tc, tf, tk = Temperature(c, "C"), Temperature(f, "F"), Temperature(k, "K")
        assert tc == tf == tk
        assert not (tc != tf)
        assert not (tf != tk)

    def test_example_from_assignment(self):
        assert Temperature(0, "C") == Temperature(32, "F")

    def test_inequality(self):
        assert Temperature(0, "C") != Temperature(33, "F")

    def test_ordering_mixed_units(self):
        cold = Temperature(0, "C")
        warm = Temperature(80, "F")  # about 26.7 C
        hot = Temperature(400, "K")  # about 126.85 C
        assert cold < warm < hot
        assert cold <= warm <= hot
        assert hot > warm > cold
        assert hot >= warm >= cold
        assert not (hot < warm)
        assert not (cold > warm)

    def test_equal_values_satisfy_le_and_ge(self):
        a, b = Temperature(100, "C"), Temperature(212, "F")
        assert a <= b and a >= b
        assert not (a < b) and not (a > b)

    def test_tolerance_is_applied(self):
        a = Temperature(300.0, "K")
        b = Temperature(300.0 + 1e-12, "K")
        assert a == b
        assert not (a < b) and not (a > b)

    def test_difference_above_tolerance_is_not_equal(self):
        assert Temperature(300.0, "K") != Temperature(300.0 + 1e-6, "K")

    @pytest.mark.parametrize("other", [5, 5.0, "5 C", None, (5, "C")])
    def test_comparison_with_non_temperature(self, other):
        t = Temperature(5, "C")
        assert t.__eq__(other) is NotImplemented
        assert t.__ne__(other) is NotImplemented
        assert t.__lt__(other) is NotImplemented
        assert t.__le__(other) is NotImplemented
        assert t.__gt__(other) is NotImplemented
        assert t.__ge__(other) is NotImplemented

    def test_eq_with_non_temperature_is_false(self):
        assert (Temperature(5, "C") == 5) is False
        assert (Temperature(5, "C") != 5) is True

    def test_ordering_with_non_temperature_raises(self):
        with pytest.raises(TypeError):
            Temperature(5, "C") < 5


# ----------------------------------------------------------------------
# 6. Formatting
# ----------------------------------------------------------------------
class TestFormatting:
    def test_str_two_decimals(self):
        assert str(Temperature(25, "C")) == "25.00 °C"

    def test_str_rounds(self):
        assert str(Temperature(36.666, "c")) == "36.67 °C"

    @pytest.mark.parametrize(
        "value, unit, expected",
        [(98.6, "F", "98.60 °F"), (273.15, "K", "273.15 K")],
    )
    def test_str_other_units(self, value, unit, expected):
        assert str(Temperature(value, unit)) == expected

    def test_repr(self):
        assert repr(Temperature(25, "C")) == "Temperature(25.0, 'C')"

    def test_repr_normalises_unit(self):
        assert repr(Temperature(300, "k")) == "Temperature(300.0, 'K')"

    def test_repr_is_evaluable(self):
        t = Temperature(98.6, "F")
        assert eval(repr(t)) == t
