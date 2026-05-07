from __future__ import annotations

from .models import DesignInput


def make_local_report(
    d: DesignInput,
    break_p: float,
    capture_p: float,
    damage: float,
    clogging: float,
    spatial: float,
    score: float,
    recommendations: list[str],
    risks: list[str],
    patent_points: list[str],
) -> str:
    """Generate a patent-style local report without calling any LLM."""
    rec_text = "\n".join(f"- {x}" for x in recommendations)
    risk_text = "\n".join(f"- {x}" for x in risks)
    point_text = "\n".join(f"- {x}" for x in patent_points)

    return f"""
# 红花花丝双侧脉冲气流采摘与收集方案报告

## 一、核心方案
本方案采用双侧相向布置的脉冲气流装置，在宽度约 {d.picking_zone_width_cm:.1f} cm 的采摘区两侧设置收集腔室。
两侧脉冲气流以约 {d.pulse_frequency_hz:.1f} Hz 的频率和 {d.pulse_pressure_kpa:.1f} kPa 的压力交替或协同作用于花丝，
使花丝产生周期性大角度弯折，并通过疲劳断裂实现柔性分割。脱落花丝随后在气流诱导和导流板约束下进入两侧收集腔室。

## 二、仿真启发式评估
- 花丝疲劳断裂概率：{break_p:.2f}
- 两侧腔室捕获概率：{capture_p:.2f}
- 植株/花冠损伤风险：{damage:.2f}
- 收集入口堵塞风险：{clogging:.2f}
- 空间可布置性：{spatial:.2f}
- 综合评分：{score:.1f} / 100

## 三、推荐优化
{rec_text}

## 四、主要风险
{risk_text}

## 五、可用于专利交底的创新点
{point_text}

## 六、下一步实验
建议用高速相机记录花丝在不同脉冲频率和压力下的弯折角度、断裂时间和脱落轨迹，
并用实际捕获率反向修正本项目中的启发式参数。
""".strip()
