import logging
from typing import List, Optional

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from models import Ingredients, Recipe

from .custom_scraper import CustomScraper

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class WprmScraper(CustomScraper):
    base_urls: List[str] = [
        "https://hebbarskitchen.com",
        "https://www.vegrecipesofindia.com",
    ]

    def __init__(self):
        pass

    def scrape(self, url) -> Recipe:
        try:
            html: str = self.get_html_content(url)

            soup = BeautifulSoup(html, "html.parser")
            recipe_name_tag: Optional[Tag] = soup.find(class_="wprm-recipe-name")
            if recipe_name_tag:
                recipe_name: str = recipe_name_tag.text
            else:
                recipe_name: str = ""

            ingredients: Optional[Ingredients] = self.extract_ingredients(soup)
            instructions: Optional[List[str]] = self.extract_instructions(soup)

            if not ingredients:
                raise RuntimeError(f"Could not get ingredients for {url}")

            if not ingredients.measured_ingredients:
                raise RuntimeError(f"Could not get ingredients for {url}")

            if not instructions:
                raise RuntimeError(f"Could not extract instructions for {url}")

            cuisine: Optional[str] = self.extract_cuisine(soup)

            recipe = Recipe(
                title=recipe_name,
                url=url,
                measuredIngredients=ingredients.measured_ingredients,
                ingredients=ingredients.ingredients or [],
                instructions="\n".join(instructions),
                cuisine=cuisine,
            )

            return recipe

        except Exception as e:
            raise RuntimeError(e)

    def extract_ingredients(self, soup: BeautifulSoup) -> Optional[Ingredients]:
        ingredients_container: Optional[Tag] = soup.find(
            class_="wprm-recipe-ingredients-container"
        )
        if not ingredients_container:
            return None

        ingredient_groups: ResultSet = ingredients_container.find_all(
            class_="wprm-recipe-ingredient-group"
        )

        ingredients: List[str] = []
        measured_ingredients: List[str] = []

        for i in ingredient_groups:
            i: Tag
            lis: ResultSet = i.find_all("li")
            for li in lis:
                li: Tag
                amount: str = ""
                unit: str = ""
                name: str = ""

                amount_tag: Optional[Tag] = li.find(
                    class_="wprm-recipe-ingredient-amount"
                )
                if amount_tag:
                    amount = amount_tag.text

                unit_tag: Optional[Tag] = li.find(class_="wprm-recipe-ingredient-unit")
                if unit_tag:
                    unit = unit_tag.text

                name_tag: Optional[Tag] = li.find(class_="wprm-recipe-ingredient-name")
                if name_tag:
                    name = name_tag.text

                measured_ingredient: str = " ".join([a for a in [amount, unit, name]])
                measured_ingredients.append(measured_ingredient)

                ingredients.append(name)

        return Ingredients(
            ingredients=ingredients, measured_ingredients=measured_ingredients
        )

    def extract_instructions(self, soup: BeautifulSoup) -> Optional[List[str]]:
        instruction_container: Optional[Tag] = soup.find(
            class_="wprm-recipe-instructions-container"
        )

        if not instruction_container:
            return None

        instruction_groups: ResultSet = instruction_container.find_all(
            class_="wprm-recipe-instruction-group"
        )

        instructions: List[str] = []

        for i in instruction_groups:
            i: Tag
            group_name_tag: Optional[Tag] = i.find(class_="wprm-recipe-group-name")
            if group_name_tag:
                group_name: str = group_name_tag.text
                instructions.append(group_name.capitalize())

            recipe_instruction: ResultSet = i.find_all(
                class_="wprm-recipe-instructions"
            )
            for r in recipe_instruction:
                instructions.append(r.text.capitalize())

        return instructions

    def extract_cuisine(self, soup: BeautifulSoup) -> Optional[str]:
        cuisine_tag: Optional[Tag] = soup.find(class_="wprm-recipe-cuisine")
        return cuisine_tag.text.capitalize() if cuisine_tag else None
