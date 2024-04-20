from typing import IO

# 10mb
MAX_FILE_SIZE = 10 * 1024 * 1024
# 1mb
FILE_CHUNK_SIZE = 1024 * 1024


class EmojiSizeValidator:
    def __init__(self, stream: IO[bytes]) -> None:
        self.stream = stream

    def is_size_valid(self) -> bool:
        total_size = 0
        while True:
            chunk = self.stream.read(FILE_CHUNK_SIZE)
            if not chunk:
                break
            total_size += len(chunk)
            if total_size > MAX_FILE_SIZE:
                self.stream.close()
                return False
        return True
