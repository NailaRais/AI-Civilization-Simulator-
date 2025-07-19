import os
from google import genai

class GeminiAPI:
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Gemini API key must be provided or set in GEMINI_API_KEY environment variable.")
        self.api_key = api_key

    def _generate(self, prompt):
        try:
            response = genai.chat(
                api_key=self.api_key,
                model="chat-bison-001",  # Use model name compatible with older SDK
                prompt=prompt,
                stream=False
            )
            return response.get("text", "").strip()
        except Exception as e:
            print(f"Generation error: {e}")
            return None

    def rate_society(self, society_summary):
        prompt = f"Rate this society's ethics on a scale of 1 to 10:\n{society_summary}\nScore:"
        try:
            score_text = self._generate(prompt)
            score = float(score_text)
            if score < 1 or score > 10:
                raise ValueError("Score out of expected range")
            return score
        except Exception as e:
            print(f"Rating error: {e}")
            return None

    def ask_policy_question(self, question):
        prompt = f"In a fair society, answer the following question with Yes, No, or Explain:\n{question}"
        return self._generate(prompt)

    def suggest_policy_change(self, society_summary):
        prompt = (
            f"The following society collapsed:\n{society_summary}\n"
            "Explain why it failed and suggest one policy change to improve it."
        )
        return self._generate(prompt)

    def summarize_findings(self, findings_text):
        prompt = f"Summarize the key findings from the following text:\n{findings_text}"
        return self._generate(prompt)
