from enum import Enum


# currently not used - its here only for the information
class Tier(Enum):
    FREE = 1
    PREMIUM = 2
    BUSINESS = 3

    @classmethod
    def from_string(cls, string):
        return cls[string.upper()]

    @classmethod
    def to_string(cls, value):
        return cls(value).name.lower()