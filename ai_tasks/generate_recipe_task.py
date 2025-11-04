import logging
from typing import Optional, cast

from google.genai import types

from models import Recipe

from .ai_task import AiTask

logging.basicConfig(level=logging.INFO)
logging.getLogger("google_genai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


class GenerateRecipeTask(AiTask):
    def __init__(self, api_key: str, model: str) -> None:
        super().__init__(api_key, model)
        self.logger = logging.getLogger(__name__)

    def prompt(self):
        return """
        You are a world-class culinary expert and recipe generator. Your task is to generate a complete, authentic recipe based on the user's request. The recipe should be for 2 average adult servings.

        You MUST analyze the request and return the entire recipe as a **single JSON object** that strictly conforms to the provided schema. Do not include any introductory text, markdown formatting (like JSON blockquotes), or explanations outside of the JSON object.

        The fields to be generated are:
        * **title** (string): The official, proper name of the dish.
        * **ingredients** (List[string]): List all base ingredients in singular form, stripping all quantities and measurements (e.g., ["chicken breast", "onion", "carrot"]).
        * **measuredIngredients** (List[string]): List all ingredients with precise quantities and units (e.g., ["1.5 lbs boneless chicken breast", "1 large chopped onion", "3 medium carrots"]).
        * **cuisine** (string): Identify the traditional cuisine of the dish (e.g., "Italian", "Mexican").
        * **instructions** (string): A single string containing clear, numbered, step-by-step instructions. Use '\n' for line breaks between steps.

        **Required Output:**
        Return ONLY a single Python dictionary that conforms to the provided JSON schema. Do not include any introductory text, markdown formatting (like JSON blockquotes), or explanations.

        Example of Required Output Format (for reference):
        {{
            "title": "Chicken Tikka Masala"
            "cuisine": "indian",
            "ingredients": ["chicken breast", "tomato sauce", "ginger", "turmeric", "heavy cream", "salt", "pepper"]
            "measuredIngredients": ["1.5 lbs boneless chicken breast", "1 large chopped onion", "3 medium carrots"]
            "instructions": "Cut the chicken\nMarinade the chicken\nCook the chicken"
        }}.
        """

    def ai_request(self, user_input: str) -> Optional[Recipe]:
        config = types.GenerateContentConfig(
            system_instruction=self.prompt(),
            response_mime_type="application/json",
            response_schema=Recipe,
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=user_input,
                config=config,
            )
            if response and response.parsed:
                recipe: Recipe = cast(Recipe, response.parsed)
                return recipe
            else:
                return None
        except Exception as e:
            raise RuntimeError(f"Recipe generation failed with error {e}")
