from dataclasses import dataclass, asdict


@dataclass
class ImagePreview:
    id: str
    data: bytes

    def __str__(self) -> str:
        return str(asdict(self))
