import logging
from typing import List, Optional, cast

from google.genai import types

from models.data_models import RecipeDetails

from .ai_task import AiTask

logging.basicConfig(level=logging.INFO)
logging.getLogger("google_genai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


class ExtractRecipeDetailsTask(AiTask):
    def __init__(self, api_key: str, model: str) -> None:
        super().__init__(api_key, model)
        self.logger = logging.getLogger(__name__)

    def prompt(self, dish_name: str, ingredients: List[str]) -> str:
        prompt = f"""
            You are an ingredient extraction expert and culinary analyst. Your task is to process the following dish name and JSON list of recipe ingredients.

            **Dish Name:** {dish_name}

            **Input JSON:**
            {ingredients}

            **Part 1: Cuisine Detection**
            Analyze the **Dish Name** and the ingredients to determine the most likely **cuisine type** (e.g., Italian, Mexican, Indian, Thai, French).

            **Part 2: Ingredient Extraction**
            For each string in the list, extract and return **only the base ingredient name in singular form**.
            You must strip away all measurements, quantities, units, preparation instructions, and parenthetical notes. You must keep the cut of meat including ground meat (e.g., 'ground beef', 'chicken breast').

            **Required Output:**
            Return ONLY a single Python dictionary that conforms to the provided JSON schema. Do not include any introductory text, markdown formatting (like JSON blockquotes), or explanations.

            Example of Required Output Format (for reference):
            {{
                "cuisine": "indian",
                "ingredients_list": ["chicken breast", "tomato sauce", "ginger", "turmeric", "heavy cream", "salt", "pepper"]
            }}.
        """

        return prompt

    def ai_request(
        self,
        dish_name: str,
        ingredients: List[str],
    ) -> Optional[RecipeDetails]:
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RecipeDetails,
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=self.prompt(dish_name, ingredients),
                config=config,
            )
            if response and response.parsed:
                recipe_details: RecipeDetails = cast(RecipeDetails, response.parsed)
                return recipe_details
            else:
                return None
        except Exception as e:
            raise RuntimeError(f"Extract recipe details request failed with error {e}")
