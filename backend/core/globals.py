from enum import Enum

# DB Constants
DB_TABLE_NAME = ""
DB_INDEX_USERNAME = "username-index"
DB_PREFIX_USER = "USER#"
DB_PREFIX_SHOPPING_LIST = "SHOPPING_LIST#"
DB_PREFIX_RECIPE = "RECIPE#"
DB_PREFIX_ITEM = "ITEM#"

ItemType = Enum('ItemType', ['user', 'list', 'recipe'])

ALLOWED_OCR_CONTENT_TYPES = ["image/jpeg", "image/png", "image/jpg"]

UNIT_ABBREVIATIONS_PLURAL = {
    "cups": "c",
    "tablespoons": "tbsp",
    "teaspoons": "tsp",
    "pounds": "lb",
    "ounces": "oz",
    "quarts": "qt",
    "gallons": "gal",
    "liters": "l",
    "milliliters": "ml",
    "grams": "g",
    "kilograms": "kg",
    "milligrams": "mg",
    "inches": "in",
    "centimeters": "cm",
    "millimeters": "mm",
    "pints": "pt",
    "fluid ounces": "fl oz",
    "pinches": "pinch",
    "handfuls": "handful",
    "sticks": "stick",
    "stalks": "stalk",
    "cloves": "clove",
    "heads": "head",
    "slices": "slice",
    "pieces": "piece",
    "cans": "can",
    "bottles": "bottle",
    "boxes": "box",
    "bags": "bag",
    "packages": "package",
    "containers": "container",
}

UNIT_ABBREVIATIONS_TO_WORD = {
    "c": "cups",
    "tbsp": "tablespoons",
    "tsp": "teaspoons",
    "lb": "pounds",
    "oz": "ounces",
    "qt": "quarts",
    "gal": "gallons",
    "l": "liters",
    "ml": "milliliters",
    "g": "grams",
    "kg": "kilograms",
    "mg": "milligrams",
    "in": "inches",
    "cm": "centimeters",
    "mm": "millimeters",
    "pt": "pints",
    "fl oz": "fluid ounces",
    "pinch": "pinches",
    "handful": "handfuls",
    "stick": "sticks",
    "stalk": "stalks",
    "clove": "cloves",
    "head": "heads",
    "slice": "slices",
    "piece": "pieces",
    "x": "unit", # for items like "2 x eggs", unique to this dict
    "can": "cans",
    "bottle": "bottles",
    "box": "boxes",
    "bag": "bags",
    "package": "packages",
    "container": "containers",
}

UNIT_SINGULAR_TO_PLURAL = {
    "cup": "cups",
    "tablespoon": "tablespoons",
    "teaspoon": "teaspoons",
    "pound": "pounds",
    "ounce": "ounces",
    "quart": "quarts",
    "gallon": "gallons",
    "liter": "liters",
    "milliliter": "milliliters",
    "gram": "grams",
    "kilogram": "kilograms",
    "milligram": "milligrams",
    "inch": "inches",
    "centimeter": "centimeters",
    "millimeter": "millimeters",
    "pint": "pints",
    "fluid ounce": "fluid ounces",
    "pinch": "pinches",
    "handful": "handfuls",
    "stick": "sticks",
    "stalk": "stalks",
    "clove": "cloves",
    "head": "heads",
    "slice": "slices",
    "piece": "pieces",
    "can": "cans",
    "bottle": "bottles",
    "box": "boxes",
    "bag": "bags",
    "package": "packages",
    "container": "containers",
}