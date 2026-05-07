from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv

from honghua_pulse_agent import DesignInput, PulseHarvestWorkflow
from honghua_pulse_agent.llm import MiMoClient, enhance_report_with_mimo

load_dotenv()

st.set_page_config(page_title="Honghua Pulse Agent", page_icon="🌺", layout="wide")

st.title("🌺 Honghua Pulse Agent")
st.caption("AI Agent + 物理启发式仿真：红花花丝双侧脉冲气流柔性分割与收集方案")

with st.sidebar:
    st.header("结构约束")
    picking_zone_width_cm = st.slider("采摘区宽度 cm", 8.0, 30.0, 16.0, 0.5)
    left_chamber_width_cm = st.slider("左侧收集腔 cm", 8.0, 35.0, 23.0, 0.5)
    right_chamber_width_cm = st.slider("右侧收集腔 cm", 8.0, 35.0, 23.0, 0.5)
    min_filament_to_floor_cm = st.slider("最低花丝到底部高度差 cm", 4.0, 25.0, 10.0, 0.5)

    st.header("气流参数")
    pulse_pressure_kpa = st.slider("脉冲压力 kPa", 5.0, 70.0, 32.0, 1.0)
    pulse_frequency_hz = st.slider("脉冲频率 Hz", 1.0, 30.0, 12.0, 0.5)
    duty_cycle = st.slider("占空比", 0.05, 0.95, 0.38, 0.01)
    nozzle_angle_deg = st.slider("喷嘴角度 °", 0.0, 80.0, 38.0, 1.0)
    nozzle_distance_cm = st.slider("喷嘴距离 cm", 2.0, 18.0, 7.5, 0.5)
    airflow_balance = st.slider("左右气流平衡系数", 0.1, 1.5, 0.92, 0.01)

    st.header("花丝与收集")
    filament_length_cm = st.slider("花丝长度 cm", 0.5, 8.0, 3.2, 0.1)
    filament_diameter_mm = st.slider("花丝直径 mm", 0.1, 1.5, 0.45, 0.05)
    filament_fatigue_resistance = st.slider("花丝疲劳抗性", 0.05, 1.5, 0.52, 0.01)
    collection_inlet_height_cm = st.slider("收集入口高度 cm", 1.0, 18.0, 7.0, 0.5)
    guide_plate_angle_deg = st.slider("导流板角度 °", 0.0, 75.0, 28.0, 1.0)

    use_mimo = st.checkbox("Use MiMo enhanced report", value=False)

design = DesignInput(
    picking_zone_width_cm=picking_zone_width_cm,
    left_chamber_width_cm=left_chamber_width_cm,
    right_chamber_width_cm=right_chamber_width_cm,
    min_filament_to_floor_cm=min_filament_to_floor_cm,
    pulse_pressure_kpa=pulse_pressure_kpa,
    pulse_frequency_hz=pulse_frequency_hz,
    duty_cycle=duty_cycle,
    nozzle_angle_deg=nozzle_angle_deg,
    nozzle_distance_cm=nozzle_distance_cm,
    airflow_balance=airflow_balance,
    filament_length_cm=filament_length_cm,
    filament_diameter_mm=filament_diameter_mm,
    filament_fatigue_resistance=filament_fatigue_resistance,
    collection_inlet_height_cm=collection_inlet_height_cm,
    guide_plate_angle_deg=guide_plate_angle_deg,
)

workflow = PulseHarvestWorkflow()
result = workflow.run(design)

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("综合评分", f"{result.overall_score:.1f}/100")
m2.metric("断裂概率", f"{result.break_probability:.2f}")
m3.metric("捕获概率", f"{result.capture_probability:.2f}")
m4.metric("损伤风险", f"{result.damage_risk:.2f}")
m5.metric("堵塞风险", f"{result.clogging_risk:.2f}")

left, right = st.columns([1, 1])

with left:
    st.subheader("Agent 推荐")
    for item in result.recommendations:
        st.write("✅ " + item)

    st.subheader("风险审查")
    for item in result.risks:
        st.write("⚠️ " + item)

    st.subheader("专利式创新点")
    for item in result.patent_points:
        st.write("💡 " + item)

with right:
    st.subheader("结构示意")
    total_width = design.left_chamber_width_cm + design.picking_zone_width_cm + design.right_chamber_width_cm
    st.markdown(
        f"""
```text
左收集腔 {design.left_chamber_width_cm:.1f}cm | 采摘区 {design.picking_zone_width_cm:.1f}cm | 右收集腔 {design.right_chamber_width_cm:.1f}cm
<------------------------- 总宽约 {total_width:.1f}cm ------------------------->

        脉冲喷嘴  >>>  花丝区域  <<<  脉冲喷嘴
              \\       |||||       /
               \\      |||||      /
                \\____导流进入两侧收集腔____/
```
"""
    )

st.subheader("Markdown 技术报告")
report = result.local_report

if use_mimo:
    client = MiMoClient()
    if client.available:
        with st.spinner("Calling Xiaomi MiMo API..."):
            try:
                report = enhance_report_with_mimo(result.local_report, client)
            except Exception as exc:
                st.error(f"MiMo API 调用失败，已回退到本地报告：{exc}")
    else:
        st.warning("未检测到 XIAOMI_MIMO_API_KEY，已使用本地 ReportAgent。")

st.markdown(report)
st.download_button("下载报告 Markdown", report, file_name="honghua_pulse_report.md")
