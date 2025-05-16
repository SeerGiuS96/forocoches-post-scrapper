from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

class ContentCategory(Enum):
    HOUSING = auto()
    RELATIONSHIP = auto()
    MARRIAGE = auto()
    GENERAL = auto()

@dataclass
class User:
    username: str
    join_date: datetime = None

@dataclass
class Post:
    id: str
    user: User
    content: str
    timestamp: datetime
    category: ContentCategory = None
    quotes: list[str] = None
    replies_to: list[str] = None