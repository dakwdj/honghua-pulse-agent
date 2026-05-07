from __future__ import annotations

import os
from typing import Any

import requests


class MiMoClient:
    """Small OpenAI-compatible client for Xiaomi MiMo.

    It deliberately uses requests instead of a heavy SDK so the demo remains simple.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout: int = 60,
    ) -> None:
        self.api_key = api_key or os.getenv("XIAOMI_MIMO_API_KEY")
        self.base_url = (base_url or os.getenv("XIAOMI_MIMO_BASE_URL") or "https://api.xiaomimimo.com/v1").rstrip("/")
        self.model = model or os.getenv("XIAOMI_MIMO_MODEL") or "mimo-v2.5-pro"
        self.timeout = timeout

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def chat(self, messages: list[dict[str, str]], temperature: float = 0.2) -> str:
        if not self.api_key:
            raise RuntimeError("XIAOMI_MIMO_API_KEY is not set.")

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


def enhance_report_with_mimo(local_report: str, client: MiMoClient | None = None) -> str:
    client = client or MiMoClient()
    system = (
        "你是一名农业机器人与专利交底书写作助手。"
        "请在不夸大实验结果的前提下，增强方案表达，突出 Agent 工作流、工程约束、创新点和下一步验证计划。"
    )
    user = f"""
请将下面的本地报告改写成 GitHub 项目展示用的技术说明。要求：
1. 保留所有关键参数和风险；
2. 不要声称已经完成真实田间验证；
3. 强调这是可运行的 AI Agent + 物理启发式仿真 Demo；
4. 输出中文 Markdown。

{local_report}
"""
    return client.chat(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
    )
