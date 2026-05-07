from __future__ import annotations

import math
from .models import DesignInput


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def bending_energy_index(d: DesignInput) -> float:
    """Estimate relative bending energy induced by two opposite pulsed jets.

    This is not a CFD solver. It is a compact engineering heuristic for early-stage
    concept comparison. The formula rewards high pulse pressure, usable nozzle
    angle, longer filament length, and balanced left/right jets.
    """
    pressure_term = math.sqrt(d.pulse_pressure_kpa / 30.0)
    frequency_term = math.log1p(d.pulse_frequency_hz) / math.log1p(12.0)
    duty_term = 1.0 - abs(d.duty_cycle - 0.38) * 1.4
    angle_term = math.sin(math.radians(d.nozzle_angle_deg + 8.0))
    distance_term = 1.0 / (1.0 + (d.nozzle_distance_cm / 12.0) ** 2)
    length_term = math.sqrt(d.filament_length_cm / 3.0)
    balance_penalty = 1.0 - abs(d.airflow_balance - 1.0) * 0.55

    raw = (
        pressure_term
        * frequency_term
        * max(0.15, duty_term)
        * max(0.1, angle_term)
        * distance_term
        * length_term
        * max(0.25, balance_penalty)
    )
    return raw / max(0.15, d.filament_fatigue_resistance)


def break_probability(d: DesignInput) -> float:
    """Probability-like score for fatigue separation of filaments."""
    energy = bending_energy_index(d)
    return clamp(logistic((energy - 0.55) * 5.2))


def spatial_feasibility(d: DesignInput) -> float:
    """Score whether the chamber and guide layout fits the tight plant geometry."""
    total_width = (
        d.picking_zone_width_cm + d.left_chamber_width_cm + d.right_chamber_width_cm
    )
    width_ok = clamp((70.0 - abs(total_width - 62.0)) / 70.0)
    height_ok = clamp((d.min_filament_to_floor_cm - 4.5) / 9.0)
    inlet_ok = clamp(1.0 - abs(d.collection_inlet_height_cm - 7.0) / 10.0)
    return clamp(0.35 * width_ok + 0.35 * height_ok + 0.30 * inlet_ok)


def capture_probability(d: DesignInput) -> float:
    """Estimate probability that separated filaments enter side collection chambers."""
    inlet_match = clamp(1.0 - abs(d.collection_inlet_height_cm - 0.7 * d.min_filament_to_floor_cm) / 10.0)
    guide_term = math.cos(math.radians(abs(d.guide_plate_angle_deg - 30.0)))
    angle_term = math.cos(math.radians(abs(d.nozzle_angle_deg - 40.0)))
    chamber_term = clamp((d.left_chamber_width_cm + d.right_chamber_width_cm) / 46.0)
    balance_term = clamp(1.0 - abs(d.airflow_balance - 1.0) * 0.7)

    return clamp(
        0.32 * inlet_match
        + 0.22 * max(0.0, guide_term)
        + 0.18 * max(0.0, angle_term)
        + 0.16 * chamber_term
        + 0.12 * balance_term
    )


def damage_risk(d: DesignInput) -> float:
    """Estimate risk of damaging flower crown or nearby plant tissue."""
    pressure_risk = clamp((d.pulse_pressure_kpa - 28.0) / 35.0)
    close_nozzle_risk = clamp((7.0 - d.nozzle_distance_cm) / 7.0)
    angle_risk = clamp((d.nozzle_angle_deg - 55.0) / 30.0)
    return clamp(0.45 * pressure_risk + 0.35 * close_nozzle_risk + 0.20 * angle_risk)


def clogging_risk(d: DesignInput) -> float:
    """Estimate risk of filament accumulation at the chamber inlet."""
    low_height_risk = clamp((7.0 - d.collection_inlet_height_cm) / 7.0)
    narrow_side_risk = clamp((36.0 - (d.left_chamber_width_cm + d.right_chamber_width_cm)) / 36.0)
    guide_risk = clamp(abs(d.guide_plate_angle_deg - 30.0) / 45.0)
    return clamp(0.42 * low_height_risk + 0.30 * narrow_side_risk + 0.28 * guide_risk)


def overall_score(d: DesignInput) -> float:
    b = break_probability(d)
    c = capture_probability(d)
    damage = damage_risk(d)
    clog = clogging_risk(d)
    spatial = spatial_feasibility(d)
    return round(100.0 * clamp(0.30 * b + 0.30 * c + 0.22 * spatial + 0.10 * (1 - damage) + 0.08 * (1 - clog)), 1)
