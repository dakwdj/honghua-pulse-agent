from __future__ import annotations

from dataclasses import dataclass

from .models import DesignInput, DesignResult
from .physics import (
    break_probability,
    capture_probability,
    damage_risk,
    clogging_risk,
    spatial_feasibility,
    overall_score,
)
from .report import make_local_report


@dataclass
class RequirementAgent:
    def run(self, d: DesignInput) -> list[str]:
        notes = []
        if d.min_filament_to_floor_cm <= 10:
            notes.append("底部高度差较小，不建议增加独立封闭收集仓，应采用侧向就近收集。")
        if d.picking_zone_width_cm <= 18:
            notes.append("采摘区较窄，喷嘴和导流结构应尽量薄型化，避免侵入花冠。")
        if abs(d.left_chamber_width_cm - d.right_chamber_width_cm) > 5:
            notes.append("左右收集腔尺寸差异较大，应重新平衡两侧气流和入口面积。")
        return notes


@dataclass
class GeometryAgent:
    def run(self, d: DesignInput) -> list[str]:
        tips = []
        if d.collection_inlet_height_cm > d.min_filament_to_floor_cm:
            tips.append("收集入口高于最低花丝，建议降低入口或采用上缘倒角导流。")
        if d.nozzle_distance_cm < 5.5:
            tips.append("喷嘴距离偏近，可能造成局部冲击损伤，建议增加缓冲导流面。")
        if d.guide_plate_angle_deg < 15 or d.guide_plate_angle_deg > 45:
            tips.append("导流板角度偏离推荐区间，建议保持在 25°–35° 附近以减少反弹。")
        return tips


@dataclass
class AirflowAgent:
    def run(self, d: DesignInput) -> list[str]:
        tips = []
        if d.pulse_frequency_hz < 6:
            tips.append("脉冲频率偏低，花丝疲劳累积不足，可提高到 8–15 Hz。")
        if d.pulse_pressure_kpa > 45:
            tips.append("压力较高，虽然有利于断裂，但会增加花冠损伤和飞散风险。")
        if abs(d.airflow_balance - 1.0) > 0.2:
            tips.append("左右气流不平衡，花丝可能偏向单侧并造成漏收。")
        return tips


@dataclass
class RiskAgent:
    def run(self, damage: float, clogging: float, spatial: float) -> list[str]:
        risks = []
        if damage > 0.45:
            risks.append("花冠或植株损伤风险偏高，需要降低压力、增加喷嘴距离或使用扩散喷口。")
        if clogging > 0.40:
            risks.append("收集入口存在堵塞风险，建议增加入口圆角、负压辅助或可拆卸滤网。")
        if spatial < 0.55:
            risks.append("空间可布置性不足，应优先压缩喷嘴厚度，避免增加独立腔室。")
        if not risks:
            risks.append("当前参数下没有明显高风险项，但仍需通过实物实验验证。")
        return risks


@dataclass
class PatentAgent:
    def run(self, d: DesignInput) -> list[str]:
        return [
            "双侧相向脉冲气流协同作用，使柔性花丝发生周期性大角度弯折并疲劳断裂。",
            "采摘区与两侧收集腔室一体化布置，使分割后的花丝就近进入收集腔，减少二次转运结构。",
            "通过喷嘴角度、脉冲频率、导流板角度和入口高度的联合调节，提高分割效率与收集稳定性。",
            "在低高度差条件下避免独立封闭仓，采用侧向腔室与导流板实现紧凑收集。",
        ]


class PulseHarvestWorkflow:
    """A lightweight multi-agent workflow for concept design."""

    def __init__(self) -> None:
        self.requirement_agent = RequirementAgent()
        self.geometry_agent = GeometryAgent()
        self.airflow_agent = AirflowAgent()
        self.risk_agent = RiskAgent()
        self.patent_agent = PatentAgent()

    def run(self, d: DesignInput) -> DesignResult:
        b = break_probability(d)
        c = capture_probability(d)
        damage = damage_risk(d)
        clogging = clogging_risk(d)
        spatial = spatial_feasibility(d)
        score = overall_score(d)

        recommendations = []
        recommendations.extend(self.requirement_agent.run(d))
        recommendations.extend(self.geometry_agent.run(d))
        recommendations.extend(self.airflow_agent.run(d))
        if not recommendations:
            recommendations.append("当前参数较均衡，建议优先开展小样机实验验证断裂时间与捕获率。")

        risks = self.risk_agent.run(damage, clogging, spatial)
        patent_points = self.patent_agent.run(d)
        local_report = make_local_report(
            d=d,
            break_p=b,
            capture_p=c,
            damage=damage,
            clogging=clogging,
            spatial=spatial,
            score=score,
            recommendations=recommendations,
            risks=risks,
            patent_points=patent_points,
        )

        return DesignResult(
            break_probability=round(b, 3),
            capture_probability=round(c, 3),
            damage_risk=round(damage, 3),
            clogging_risk=round(clogging, 3),
            spatial_feasibility=round(spatial, 3),
            overall_score=score,
            recommendations=recommendations,
            risks=risks,
            patent_points=patent_points,
            local_report=local_report,
        )
