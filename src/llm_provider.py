import os
import json
import requests
from google import genai
from google.genai import types

class SwappableLLM:
    def __init__(self, provider: str = "gemini", model_name: str = "gemini-2.5-flash", api_key: str = None):
        self.provider = provider.lower()
        self.model_name = model_name
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GROQ_API_KEY")

    def generate(self, system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
        if self.provider == "gemini":
            client = genai.Client(api_key=self.api_key)
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.2,
                response_mime_type="application/json" if json_mode else "text/plain"
            )
            resp = client.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=config
            )
            return resp.text

        elif self.provider == "groq":
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.2
            }
            if json_mode:
                payload["response_format"] = {"type": "json_object"}
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=30)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]

        elif self.provider == "ollama":
            # Preserves local Ollama execution from ashankgupta/ipc_legal_chatbot
            payload = {
                "model": self.model_name,
                "prompt": f"System: {system_prompt}\nUser: {user_prompt}",
                "stream": False
            }
            if json_mode:
                payload["format"] = "json"
            r = requests.post("http://localhost:11434/api/generate", json=payload, timeout=60)
            r.raise_for_status()
            return r.json()["response"]