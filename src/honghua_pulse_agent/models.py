from __future__ import annotations

from pydantic import BaseModel, Field


class DesignInput(BaseModel):
    """Input parameters for the pulsed-air harvesting concept."""

    picking_zone_width_cm: float = Field(16.0, gt=1, description="Central picking zone width")
    left_chamber_width_cm: float = Field(23.0, gt=1)
    right_chamber_width_cm: float = Field(23.0, gt=1)
    min_filament_to_floor_cm: float = Field(10.0, gt=0)

    pulse_pressure_kpa: float = Field(32.0, gt=1, description="Pulse gauge pressure")
    pulse_frequency_hz: float = Field(12.0, gt=0.1)
    duty_cycle: float = Field(0.38, ge=0.05, le=0.95)
    nozzle_angle_deg: float = Field(38.0, ge=0, le=80)
    nozzle_distance_cm: float = Field(7.5, gt=0.5)

    filament_length_cm: float = Field(3.2, gt=0.3)
    filament_diameter_mm: float = Field(0.45, gt=0.05)
    filament_fatigue_resistance: float = Field(
        0.52,
        ge=0.05,
        le=1.5,
        description="Relative resistance; higher means harder to fatigue-break",
    )

    collection_inlet_height_cm: float = Field(7.0, gt=0.5)
    guide_plate_angle_deg: float = Field(28.0, ge=0, le=75)
    airflow_balance: float = Field(
        0.92,
        ge=0.1,
        le=1.5,
        description="1.0 means left/right pulses are well balanced",
    )


class DesignResult(BaseModel):
    break_probability: float
    capture_probability: float
    damage_risk: float
    clogging_risk: float
    spatial_feasibility: float
    overall_score: float
    recommendations: list[str]
    risks: list[str]
    patent_points: list[str]
    local_report: str
    mimo_report: str | None = None
