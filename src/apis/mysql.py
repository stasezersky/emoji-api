from typing import List, Tuple
from icecream import ic
from lib.image import Image, PersonalImage

GALLERY_TABLE = "gallery"
UPLOADS_TABLE = "uploads"
USERS_TABLE = "users"


class MySqlApi:
    # TODO implement db cursor
    def __init__(self, host: str, user: str, password: str, database: str, limit=20):
        self.limit = limit
        self.offset = 0
        pass

    # TODO implement actual query
    def get_gallery_page(self, tier: int, page_num=0) -> List[Image]:
        ic(
            f"SELECT id, preview_url, full_size_url FROM {GALLERY_TABLE} WHERE active=1 AND tier <= {tier}\
                  LIMIT {self.limit}\
                      OFFSET {page_num * self.limit}"
        )
        return [
            Image(1, "aaaa", "aaaa", "aaaa", "aaaa"),
            Image(2, "bbb", "aaaa", "aaaa", "aaaa"),
            Image(3, "ccc", "aaaa", "aaaa", "aaaa"),
        ]

    # TODO implement actual query
    def get_single_image_gallery_url(self, id: str, tier: int) -> str:
        ic(
            f"SELECT full_size_url FROM {GALLERY_TABLE} WHERE id = {id} and tier <= {tier}"
        )
        return "https://single_image_url"

    # TODO implement actual query
    def get_uploads_page(self, user_id, page_num=0) -> List[Image]:
        ic(
            f"SELECT id, preview_url, full_size_url FROM {UPLOADS_TABLE} WHERE user_id ={user_id} AND\
              active=1 AND \
                  LIMIT {self.limit}\
                      OFFSET {page_num * self.limit}"
        )
        return [
            Image(1, "aaaa", "aaaa", "aaaa"),
            Image(2, "bbb", "aaaa", "aaaa"),
            Image(3, "ccc", "aaaa", "aaaa"),
        ]

    # TODO implement actual query
    def get_single_image_uploads_url(self, user_id: str, id: str) -> Tuple[str, str]:
        ic(
            f"SELECT full_url, arn FROM {UPLOADS_TABLE} WHERE user_id = {user_id} AND id = {id}"
        )
        return "https://single_image_url", "arn:bbbbb"

    # TODO implement actual query
    def save_image_data(
        self, image: PersonalImage
    ) -> bool:
        ic(
            f"INSERT INTO {UPLOADS_TABLE} \
                ('user_id', 'id', 'preview_url', 'full_size_url', 'full_size_arn', 'preview_arn' )\
            VALUES({image.user_id}, {image.image_id}, {image.full_size_url},\
             \ {image.preview_url}, {image.full_size_arn}, {image.preview_arn})"
        )
        return True

    # TODO implement actual query
    def get_user_uploads_count(self, user_id: str) -> int:
        ic(f"SELECT upload_count FROM {USERS_TABLE} WHERE user_id = {user_id}")
        return 1
