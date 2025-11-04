from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, RootModel

from .data_models import Recipe, ShoppingListItem


class IdResponse(BaseModel):
    id: str


class RecipeResponse(RootModel):
    root: Optional[Recipe]


class RecipeListResponse(BaseModel):
    recipes: List[Recipe]


class OkResponse(BaseModel):
    ok: str = "ok"
