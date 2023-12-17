from dataclasses import dataclass
from enum import Enum


class Code(Enum):
    CODEZINE = 'codezine'

@dataclass
class NewsData():
    code: Code
    id: int
    title: str
    link: str
    date: int
    content: str
    tag_set: set[str]