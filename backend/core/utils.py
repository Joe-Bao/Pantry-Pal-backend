import time

def KeyToId(key: str) -> str:
    return key.split("#")[1]

def GetCurrentTimeInSeconds() -> int:
    return int(time.time())