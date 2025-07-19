import os
from google import genai
from google.generativeai.types import GenerationConfig

class GeminiAPI:
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Gemini API key must be provided or set in GEMINI_API_KEY environment variable.")
        genai.configure(api_key=api_key)

    def rate_society(self, society_summary):
        """
        Send a prompt to Gemini to rate the society's ethics (1-10).
        """
        prompt = f"Rate this society's ethics on a scale of 1 to 10:\n{society_summary}\nScore:"
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=GenerationConfig(
                temperature=0.3,
                max_output_tokens=10,
            )
        )
        response = model.generate_content(prompt)
        try:
            score_text = response.text.strip()
            score = float(score_text)
            if score < 1 or score > 10:
                raise ValueError("Score out of expected range")
            return score
        except Exception:
            return None

    def ask_policy_question(self, question):
        """
        Ask Gemini a yes/no/explain question about policy.
        """
        prompt = f"In a fair society, answer the following question with Yes, No, or Explain:\n{question}"
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=GenerationConfig(
                temperature=0.5,
                max_output_tokens=100,
            )
        )
        response = model.generate_content(prompt)
        return response.text.strip()

    def suggest_policy_change(self, society_summary):
        """
        Ask Gemini why a society failed and suggest one policy change.
        """
        prompt = (
            f"The following society collapsed:\n{society_summary}\n"
            "Explain why it failed and suggest one policy change to improve it."
        )
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=GenerationConfig(
                temperature=0.7,
                max_output_tokens=150,
            )
        )
        response = model.generate_content(prompt)
        return response.text.strip()

    def summarize_findings(self, findings_text):
        """
        Ask Gemini to summarize key findings for a report.
        """
        prompt = f"Summarize the key findings from the following text:\n{findings_text}"
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=GenerationConfig(
                temperature=0.5,
                max_output_tokens=150,
            )
        )
        response = model.generate_content(prompt)
        return response.text.strip()
