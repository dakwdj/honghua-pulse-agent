# Honghua Pulse Agent：红花花丝脉冲气流采摘方案 AI Agent

> 一个可运行、可展示、可继续接入 Xiaomi MiMo API 的农业机器人概念验证项目。  
> 目标：用 AI Agent + 物理启发式仿真，辅助设计“红花花丝双侧脉冲气流柔性分割与收集装置”。

## 1. 项目亮点

传统红花花丝采摘依赖人工，花丝目标细小、柔软、位于花冠内部，刚性夹持或切割容易损伤花冠与植株。  
本项目将采摘装置设计拆解为多 Agent 协作流程：

1. **RequirementAgent**：解析结构约束，例如采摘区宽度、两侧收集腔尺寸、花丝高度差等。
2. **GeometryAgent**：检查布局是否符合空间限制，输出推荐喷嘴角度、收集腔入口高度等。
3. **AirflowAgent**：基于脉冲频率、压力、喷嘴角度估算花丝弯折强度和疲劳断裂概率。
4. **CollectorAgent**：估算脱落花丝被两侧收集腔捕获的概率。
5. **RiskAgent**：识别损伤、漏收、堵塞、空间不足等风险。
6. **ReportAgent**：生成结构方案、创新点和专利交底式说明。

项目既可以纯本地运行，也可以通过 OpenAI-compatible 接口接入 Xiaomi MiMo，对方案报告进行增强生成。

## 2. 快速开始

```bash
git clone https://github.com/yourname/honghua-pulse-agent.git
cd honghua-pulse-agent

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
pip install -e .
streamlit run app.py
```

## 3. 可选：接入 Xiaomi MiMo API

复制环境变量模板：

```bash
cp .env.example .env
```

填写：

```bash
XIAOMI_MIMO_API_KEY=your_api_key_here
XIAOMI_MIMO_BASE_URL=https://api.xiaomimimo.com/v1
XIAOMI_MIMO_MODEL=mimo-v2.5-pro
```

然后在界面中勾选“Use MiMo enhanced report”。如果没有 API key，系统会自动使用本地 ReportAgent，不影响演示。

## 4. 命令行运行

```bash
python -m honghua_pulse_agent.cli examples/sample_design.json
```

输出示例：

```text
Overall score: 83.4 / 100
Break probability: 0.76
Capture probability: 0.81
Recommended concept:
双侧相向脉冲气流使花丝周期性大角度弯折并疲劳断裂，脱落花丝被邻近收集腔就近捕获。
```

## 5. 项目结构

```text
honghua-pulse-agent/
├── app.py
├── requirements.txt
├── pyproject.toml
├── .env.example
├── examples/
│   └── sample_design.json
├── src/
│   └── honghua_pulse_agent/
│       ├── agents.py
│       ├── cli.py
│       ├── llm.py
│       ├── models.py
│       ├── physics.py
│       └── report.py
└── tests/
    └── test_physics.py
```

## 6. 为什么适合作为 MiMo Token 申请项目

- **不是空项目**：包含可运行 Web Demo、CLI、测试、结构化代码和样例输入。
- **有真实场景**：面向农业机器人与柔性采摘装置，具备明确工程痛点。
- **有 Agent 流程**：需求解析、几何布局、气流机理、收集评估、风险审查、报告生成。
- **适合长链推理模型**：工程方案需要在空间、气流、材料、收集路径和专利表达之间反复权衡。
- **可持续扩展**：后续可接入 CFD 仿真、视觉识别、CAD 参数化建模和实验数据回归。

## 7. 后续路线图

- [ ] 接入真实高速相机实验数据，拟合花丝断裂模型。
- [ ] 增加喷嘴阵列优化算法。
- [ ] 输出 CAD 参数表，便于 SolidWorks / Fusion 360 建模。
- [ ] 增加多目标优化：低损伤、高捕获率、低能耗、低堵塞风险。
- [ ] 接入 Xiaomi MiMo 的多模态能力，分析样机图片与实验视频。
