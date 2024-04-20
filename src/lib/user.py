class User:
    def __init__(self, user_id: str, user_tier: int, uploads_count: int) -> None:
        self.user_id = user_id
        self.user_tier = user_tier
        self.uploads_count = uploads_count

    def can_user_upload(self) -> bool:
        if self.user_tier == 1 and self.uploads_count < 5:
            return True
        if self.user_tier == 2 and self.uploads_count < 100:
            return True
        if self.user_tier == 3:
            return True
        return False