# llm_manager.py
# 3 Farklı LLM'i yöneten modül (Main, Refiner, Supervisor)
# Her biri için isim, host, port, prompt işleyici ve görev tipi tanımı

from typing import Dict, Callable
import requests

class LLMClient:
    def __init__(self, name: str, host: str, port: int, role: str, prompt_modifier: Callable[[str], str] = None):
        self.name = name
        self.host = host
        self.port = port
        self.role = role
        self.prompt_modifier = prompt_modifier or (lambda x: x)

    def call(self, prompt: str) -> str:
        modified_prompt = self.prompt_modifier(prompt)
        url = f"http://{self.host}:{self.port}/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self.role,
            "messages": [{"role": "user", "content": modified_prompt}]
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            return f"[ERROR in LLM {self.name}] {e}"


class LLMManager:
    def __init__(self):
        self.llms: Dict[str, LLMClient] = {}

    def register_llm(self, name: str, host: str, port: int, role: str, prompt_modifier: Callable[[str], str] = None):
        self.llms[name] = LLMClient(name, host, port, role, prompt_modifier)

    def list_llms(self):
        return list(self.llms.keys())

    def get_llm(self, name: str) -> LLMClient:
        return self.llms.get(name)

    def call_llm(self, name: str, prompt: str) -> str:
        llm = self.get_llm(name)
        if llm:
            return llm.call(prompt)
        else:
            return f"[ERROR] LLM with name '{name}' not found."

# Global erişim için instance
llm_manager = LLMManager()
