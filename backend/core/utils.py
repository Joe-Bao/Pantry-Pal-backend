import time

from .globals import DB_PREFIX_RECIPE, DB_PREFIX_SHOPPING_LIST, DB_PREFIX_USER, ItemType

def KeyToId(key: str) -> str:
    return key.split("#")[1]

def GetCurrentTimeInSeconds() -> int:
    return int(time.time())

def ItemTypePrefix(type: ItemType) -> str:
    return DB_PREFIX_USER if type == ItemType.user else \
           DB_PREFIX_SHOPPING_LIST if type == ItemType.list else \
           DB_PREFIX_RECIPE