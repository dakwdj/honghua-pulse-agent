from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import DesignInput
from .agents import PulseHarvestWorkflow


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Honghua Pulse Agent on a design JSON.")
    parser.add_argument("json_path", type=Path)
    parser.add_argument("--report", action="store_true", help="Print the full local Markdown report.")
    args = parser.parse_args()

    payload = json.loads(args.json_path.read_text(encoding="utf-8"))
    design = DesignInput(**payload)
    result = PulseHarvestWorkflow().run(design)

    if args.report:
        print(result.local_report)
    else:
        print(f"Overall score: {result.overall_score} / 100")
        print(f"Break probability: {result.break_probability}")
        print(f"Capture probability: {result.capture_probability}")
        print("Recommended concept:")
        print("双侧相向脉冲气流使花丝周期性大角度弯折并疲劳断裂，脱落花丝被邻近收集腔就近捕获。")


if __name__ == "__main__":
    main()
