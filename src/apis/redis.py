from typing import List
from icecream import ic
from lib.image import Image
from lib.image_preview import ImagePreview

QUERY_CACHING = "query_caching"
EMOJI_PREVIEW = "emoji_preview"


class RedisApi:
    def __init__(self, host: str, user: str, password: str, default_expire=50000):
        pass

    def get_emoji_previews(self, ids: List[Image]) -> List[ImagePreview]:
        """
        Return a cached list of emoji previews
        """
        ic("redis.mget(ids)")
        return [
            ImagePreview("123", bytes(111)),
            ImagePreview("123", bytes(111))
        ]

    def get_query_data(self, query: str) -> List[Image]:
        """
        Return a cached list of db query results
        """
        ic("redis.get(query)")
        return [
            Image("aaa", "aaa", "aaaa", "aaaa", "aaaa"),
            Image("aaa", "aaa", "aaaa", "aaaa", "aaaa")
        ]

    def cache_query_results(self, query: str, results: List[str]) -> bool:
        """
        Caching queries for future reuse
        """
        data = {"query": results}
        ic(f"redis.mset({data})")
        return True

    def cache_emoji_preview(self, image: Image) -> bool:
        """
        Caching preview blobs for future reuse
        """
        data = {id: image.preview_url}
        ic(f"redis.mset({data})")
        return True
