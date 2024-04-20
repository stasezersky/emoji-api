from typing import Tuple
from icecream import ic

PREVIEW_PATH = "preview"
FULL_SIZE_PATH = "full_size"


class S3Api:
    def __init__(self, role_arn: str, presign_url_ttl=300):
        pass

    def save_full_size_emoji(self, id: str, data: bytes) -> Tuple[str, str]:
        ic(f"write file to {FULL_SIZE_PATH} on the graphics bucket")
        return "http://image_url", "arn"

    def save_preview_emoji(self, id: str, data: bytes) -> Tuple[str, str]:
        ic(f"write file to {PREVIEW_PATH} on the graphics bucket")
        return "http://image_url", "arn"

    def load_preview_emoji(self, id: str) -> bytes:
        ic(f"load file from {PREVIEW_PATH} on the graphics bucket")
        return bytes([123123])

    # TODO not used at the moment but can use it to manage access to private uploads
    def get_presigned_url(self, arn: str) -> str:
        ic("generates presigned url for specific amount of time")
        return "https://presigned_url"
