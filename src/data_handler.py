from typing import List
from apis.mysql import MySqlApi
from apis.redis import RedisApi
from apis.s3 import S3Api
from lib.image import Image, PersonalImage
from lib.image_preview import ImagePreview
from lib.image_minified import MinifiedImage
from lib.user import User
from icecream import ic
import uuid


class DataHandler:
    def __init__(self) -> None:
        self.db = MySqlApi("localhost", "you", "abc", "graphics")
        self.cache = RedisApi("localhost", "me", "123")
        self.s3 = S3Api("arn:11111111", 5000)
        self._fill_cache_with_previews()

    # TODO load all previews from the bucket into the cache
    def _fill_cache_with_previews(self):
        pass

    def params_to_cache_key(self, *args) -> str:
        key = '_'.join(str(arg) for arg in args)
        ic(key)
        return key

    def get_previews_from_gallery(self, user_tier: int, page_num=0) -> List[ImagePreview]:
        """
        Gets page of images from gallery according to user tier
        """
        cache_key = self.params_to_cache_key(user_tier, page_num)
        cached_images = self.cache.get_query_data(cache_key)
        if len(cached_images) >= 20:
            return self.cache.get_emoji_previews(cached_images)
        images_from_db = self.db.get_gallery_page(user_tier, page_num)
        self.cache.cache_query_results(cache_key, [image.__str__() for image in images_from_db])
        return self.cache.get_emoji_previews(images_from_db)
    
    def get_single_image_from_gallery(self, user_tier: int, image_id: str) -> str:
        """
        Gets single full size image url from gallery according to user tier
        """
        cache_key = self.params_to_cache_key(image_id, user_tier)
        cached_single_image_url = self.cache.get_query_data(cache_key)
        if cached_single_image_url:
            return cached_single_image_url[0].full_size_url
        image_url = self.db.get_single_image_gallery_url(image_id, user_tier)
        self.cache.cache_query_results(cache_key, [image_url])
        return image_url
    
    def get_previews_from_user_uploads(self, user_id: int, page_num=0) -> List[ImagePreview]:
        """
        Gets page of images from uploads according to user tier
        """
        cache_key = self.params_to_cache_key(user_id, page_num)
        cached_images = self.cache.get_query_data(cache_key)
        if len(cached_images):
            return self.cache.get_emoji_previews(cached_images)
        images_from_db = self.db.get_uploads_page(user_id, page_num)
        self.cache.cache_query_results(cache_key, [image.__str__() for image in images_from_db])
        return self.cache.get_emoji_previews(images_from_db)

    def get_single_image_from_user_uploads(self, user_id: str, image_id: str) -> str:
        """
        Gets single full size image url from user uploads
        """
        cache_key = self.params_to_cache_key(image_id, user_id)
        cached_single_image_url = self.cache.get_query_data(cache_key)
        if cached_single_image_url:
            return cached_single_image_url[0].full_size_url
        image_url, arn = self.db.get_single_image_uploads_url(user_id, image_id)
        self.cache.cache_query_results(cache_key, [image_url])
        return image_url
    
    def upload_image_to_user_uploads(self, user_id: str, user_tier: int, image: bytes) -> Image:
        """
        Validates the uploads count
        Uploads an image into the graphics bucket - full size and minified for preview
        Writes to UPLOADS table in db
        Writes the preview into the cache
        """
        uploads_count = self.db.get_user_uploads_count(user_id)
        user = User(user_id, user_tier, uploads_count)
        if user.can_user_upload():
            minified_image = MinifiedImage(image)
            image_id = str(uuid.uuid4())
            full_size_image_url, full_size_image_arn = self.s3.save_full_size_emoji(image_id, image)
            minified_image_url, minified_image_arn = self.s3.save_preview_emoji(image_id, minified_image.image)
            db_image_data = PersonalImage(str(image_id), minified_image_url, full_size_image_url,
                                          full_size_image_arn, minified_image_url, user_id)
            self.db.save_image_data(db_image_data)
            self.cache.cache_emoji_preview(db_image_data)
            return db_image_data

        raise ValueError("user can't upload more emojis")
