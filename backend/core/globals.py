from enum import Enum

# DB Constants
DB_TABLE_NAME = ""
DB_INDEX_USERNAME = "username-index"
DB_PREFIX_USER = "USER#"
DB_PREFIX_SHOPPING_LIST = "SHOPPING_LIST#"
DB_PREFIX_RECIPE = "RECIPE#"
DB_PREFIX_ITEM = "ITEM#"

ItemType = Enum('ItemType', 'user list recipe')
