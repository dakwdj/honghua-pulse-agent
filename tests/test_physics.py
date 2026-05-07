from honghua_pulse_agent.models import DesignInput
from honghua_pulse_agent.physics import (
    break_probability,
    capture_probability,
    damage_risk,
    overall_score,
)


def test_probabilities_are_in_range():
    d = DesignInput()
    for fn in [break_probability, capture_probability, damage_risk]:
        value = fn(d)
        assert 0.0 <= value <= 1.0


def test_score_is_reasonable():
    d = DesignInput()
    score = overall_score(d)
    assert 0.0 <= score <= 100.0


def test_higher_pressure_improves_break_but_increases_damage():
    low = DesignInput(pulse_pressure_kpa=15)
    high = DesignInput(pulse_pressure_kpa=55)
    assert break_probability(high) >= break_probability(low)
    assert damage_risk(high) >= damage_risk(low)
