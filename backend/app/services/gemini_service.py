import logging
from typing import Dict, Any, Optional
from app.config import settings

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.client = None

        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize Gemini SDK client: {e}")

    async def generate_portfolio_feedback(
        self,
        username: str,
        target_role: str,
        portfolio_score: float,
        existing_skills: list,
        missing_skills: list
    ) -> Dict[str, str]:
        """
        Generates qualitative career advice, portfolio commentary, and README improvement suggestions.
        """
        if not self.client:
            return self._fallback_feedback(target_role, portfolio_score, missing_skills)

        try:
            prompt = f"""
            You are a Senior Principal Engineer and Technical Hiring Manager.
            Analyze this developer profile and provide concise, high-impact career feedback.

            Developer Profile:
            - Username/Name: {username or 'Developer'}
            - Target Role: {target_role}
            - Overall Portfolio Strength Score: {portfolio_score}/100
            - Existing Skills: {', '.join(existing_skills[:10])}
            - Key Skill Gaps Identified: {', '.join([s.get('name', '') if isinstance(s, dict) else str(s) for s in missing_skills[:5]])}

            Respond strictly in valid JSON format with keys:
            1. "executive_summary": A professional string evaluation of their readiness for {target_role}.
            2. "career_advice": Actionable string advice on how to fast-track hiring potential.
            3. "readme_tips": A single string containing 2 specific tips to improve repository documentation and code presentation.
            """

            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )

            text = response.text.strip()
            # Clean JSON markdown fences if present
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

            import json
            parsed = json.loads(text)

            def to_str(val):
                if isinstance(val, list):
                    return " ".join([str(item) for item in val])
                return str(val) if val else ""

            return {
                "executive_summary": to_str(parsed.get("executive_summary")),
                "career_advice": to_str(parsed.get("career_advice")),
                "readme_tips": to_str(parsed.get("readme_tips"))
            }
        except Exception as e:
            logger.error(f"Gemini API generation error: {e}")
            return self._fallback_feedback(target_role, portfolio_score, missing_skills)

    def _fallback_feedback(self, target_role: str, score: float, missing_skills: list) -> Dict[str, str]:
        missing_names = ", ".join([s.get("name", "") if isinstance(s, dict) else str(s) for s in missing_skills[:3]])
        return {
            "executive_summary": f"Your current portfolio score of {score}/100 demonstrates strong fundamentals for the {target_role} position. Focusing on missing core technologies will elevate your profile to senior readiness.",
            "career_advice": f"Prioritize hands-on projects incorporating {missing_names or 'key stack gaps'}. Deploy complete end-to-end applications to demonstrate production competence.",
            "readme_tips": "Ensure every repository includes an architectural diagram, explicit setup instructions, dynamic badges, and clear API documentation."
        }
