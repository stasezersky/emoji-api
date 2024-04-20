from dataclasses import dataclass, asdict


@dataclass
class Image:
    image_id: str
    preview_url: str
    full_size_url: str
    full_size_arn: str
    preview_arn: str

    def __str__(self) -> str:
        return str(asdict(self))


@dataclass
class PersonalImage(Image):
    user_id: str
