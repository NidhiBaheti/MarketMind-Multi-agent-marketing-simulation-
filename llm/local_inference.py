import os, time, requests
from dotenv import load_dotenv

load_dotenv()

class UIUCChatLLM:
    def __init__(self, api_key=None,
                 model="qwen2.5:7b-instruct-fp16",
                 course_name="MarketMindd",
                 base_url="https://uiuc.chat/api/chat-api/chat"):
        self.api_key     = api_key or os.getenv("UIUC_API_KEY")
        if not self.api_key:
            raise ValueError("Missing UIUC.chat API key")
        self.model       = model
        self.course_name = course_name
        self.url         = base_url

    def generate(self, prompt: str, temperature: float = 0.6) -> str:
        payload = {
            "model":         self.model,
            "messages":      [
                {"role": "system", "content": "You are a senior brand copywriter."},
                {"role": "user",   "content": prompt}
            ],
            "api_key":       self.api_key,
            "course_name":   self.course_name,
            "stream":        False,
            "temperature":   temperature,
            "retrieval_only": False
        }

        # Try up to 3 times
        for attempt in range(1, 4):
            try:
                print(f"→ [UIUC] Attempt {attempt}, payload keys: {list(payload.keys())}")
                resp = requests.post(self.url, json=payload, timeout=10)
                print(f"← [UIUC] Status {resp.status_code}, body: {resp.text[:200]}…")
                resp.raise_for_status()
                return resp.json().get("message", "").strip()
            except requests.exceptions.HTTPError as e:
                # Server error or bad request
                print(f"[Error][UIUC] HTTP {resp.status_code} on attempt {attempt}")
                if attempt == 3:
                    raise
                time.sleep(attempt * 1.0)
            except requests.exceptions.RequestException as e:
                # Network or timeout
                print(f"[Error][UIUC] Network error: {e} (attempt {attempt})")
                if attempt == 3:
                    raise
                time.sleep(attempt * 0.5)