from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from enum import Enum


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SummaryData:
    id: int
    title: str
    uri: str
    date: int
    summary: str
    tag_set: set[str]