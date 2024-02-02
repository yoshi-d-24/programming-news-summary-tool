from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from enums.code import Code


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class NewsData:
    code: Code
    id: int
    title: str
    link: str
    date: int
    content: str
    tag_set: set[str]