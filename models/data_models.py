from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class RecipeDetails(BaseModel):
    cuisine: str
    ingredients: List[str]


class ShoppingListItem(BaseModel):
    name: str
    checked: bool


class ShoppingList(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    items: List[ShoppingListItem]


class ShoppingListList(BaseModel):
    lists: List[ShoppingList]


class Ingredients(BaseModel):
    ingredients: Optional[List[str]]
    measured_ingredients: Optional[List[str]]


class Recipe(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    url: Optional[str] = Field(default="")
    img_url: Optional[str] = Field(default="")
    ingredients: List[str] = Field(default_factory=list)
    measured_ingredients: List[str] = Field(alias="measuredIngredients")
    cuisine: Optional[str] = Field(default="")
    instructions: str

    model_config = ConfigDict({"populate_by_name": True})
