import re
import time

from .globals import DB_PREFIX_RECIPE, DB_PREFIX_SHOPPING_LIST, DB_PREFIX_USER, UNIT_ABBREVIATIONS_TO_WORD, ItemType

def KeyToId(key: str) -> str:
    return key.split("#")[1]

def GetCurrentTimeInSeconds() -> int:
    return int(time.time())

def ItemTypePrefix(type: ItemType) -> str:
    return DB_PREFIX_USER if type == ItemType.user else \
           DB_PREFIX_SHOPPING_LIST if type == ItemType.list else \
           DB_PREFIX_RECIPE

def GetQuantityFromProductSize(str: str) -> int:
    num = re.sub(r'\D', '', str)
    return 1 if num == '' else int(num)

def GetUnitFromProductSize(str: str) -> str:
    unit = re.sub(r'[^a-zA-Z]', '', str).lower()
    if unit == 'per kg':
        return 'kilograms'
    elif unit in UNIT_ABBREVIATIONS_TO_WORD:
        return UNIT_ABBREVIATIONS_TO_WORD[unit]
    else:
        return 'unit'

def roughMatchDiets(diets_list, recipe_diets):
    # Convert both lists to lowercase for case-insensitive comparison
    diets_list_lower = [diet.lower() for diet in diets_list]
    recipe_diets_lower = [diet.lower() for diet in recipe_diets]

    # Check if each diet in diets_list is roughly matched in the recipe_diets
    for diet in diets_list_lower:
        # Use regex to allow rough matching (e.g., partial matches)
        match_found = False
        for recipe_diet in recipe_diets_lower:
            if re.search(diet, recipe_diet):
                match_found = True
                break
        
        # If one diet in diets_list is not found, return False
        if not match_found:
            return False
    return True
