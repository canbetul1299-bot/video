from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from uuid import uuid4
from enum import Enum


class VideoVisibility(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    UNLISTED = "unlisted"


class VideoStatus(Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PUBLISHED = "published"
    BLOCKED = "blocked"


class VideoBase(ABC):

    @staticmethod
    def generate_video_id() -> str:
        return str(uuid4())

    def __init__(
        self,
        channel_id: str,
        title: str,
        duration_seconds: int,
        visibility: VideoVisibility = VideoVisibility.PUBLIC,
        status: VideoStatus = VideoStatus.UPLOADED
    ):
        self.video_id = self.generate_video_id()
        self.channel_id = channel_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.visibility = visibility
        self.status = status

        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.last_watched_at: Optional[datetime] = None

        self.has_subtitles = False
        self.tags: list[str] = []
        self.flags: list[str] = []

        self.view_count = 0
        self.watch_time_seconds = 0
        self.rating_total = 0
        self.rating_count = 0

        self.metadata: dict[str, str] = {}

    def process(self) -> None:
        if self.status == VideoStatus.UPLOADED:
            self.status = VideoStatus.PROCESSING
            self.updated_at = datetime.now()

    def publish(self) -> None:
        if self.status == VideoStatus.PROCESSING:
            self.status = VideoStatus.PUBLISHED
            self.updated_at = datetime.now()

    def unpublish(self) -> None:
        if self.status == VideoStatus.PUBLISHED:
            self.status = VideoStatus.PROCESSING
            self.updated_at = datetime.now()

    def block(self) -> None:
        self.status = VideoStatus.BLOCKED
        self.updated_at = datetime.now()

    def change_visibility(self, visibility: VideoVisibility) -> None:
        self.visibility = visibility
        self.updated_at = datetime.now()

    def mark_watched(self) -> None:
        self.last_watched_at = datetime.now()
        self.view_count += 1

    def add_watch_time(self, seconds: int) -> None:
        if seconds > 0:
            self.watch_time_seconds += seconds

    def enable_subtitles(self) -> None:
        self.has_subtitles = True

    def disable_subtitles(self) -> None:
        self.has_subtitles = False

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        if tag in self.tags:
            self.tags.remove(tag)

    def add_flag(self, flag: str) -> None:
        if flag not in self.flags:
            self.flags.append(flag)

    def remove_flag(self, flag: str) -> None:
        if flag in self.flags:
            self.flags.remove(flag)

    def add_rating(self, rating: int) -> None:
        if 1 <= rating <= 5:
            self.rating_total += rating
            self.rating_count += 1

    def average_rating(self) -> float:
        if self.rating_count == 0:
            return 0.0
        return self.rating_total / self.rating_count

    def add_metadata(self, key: str, value: str) -> None:
        self.metadata[key] = value

    def remove_metadata(self, key: str) -> None:
        if key in self.metadata:
            del self.metadata[key]

    def is_public(self) -> bool:
        return self.visibility == VideoVisibility.PUBLIC

    def is_private(self) -> bool:
        return self.visibility == VideoVisibility.PRIVATE

    def is_unlisted(self) -> bool:
        return self.visibility == VideoVisibility.UNLISTED

    def is_uploaded(self) -> bool:
        return self.status == VideoStatus.UPLOADED

    def is_processing(self) -> bool:
        return self.status == VideoStatus.PROCESSING

    def is_published(self) -> bool:
        return self.status == VideoStatus.PUBLISHED

    def is_blocked(self) -> bool:
        return self.status == VideoStatus.BLOCKED

    def is_valid(self) -> bool:
        if not self.title:
            return False
        if self.duration_seconds <= 0:
            return False
        return self.validate_specific_rules()

    def update_title(self, title: str) -> None:
        self.title = title
        self.updated_at = datetime.now()

    def update_duration(self, seconds: int) -> None:
        if seconds > 0:
            self.duration_seconds = seconds
            self.updated_at = datetime.now()

    def reset_stats(self) -> None:
        self.view_count = 0
        self.watch_time_seconds = 0
        self.rating_total = 0
        self.rating_count = 0

    def to_dict(self) -> dict:
        return {
            "video_id": self.video_id,
            "channel_id": self.channel_id,
            "title": self.title,
            "duration_seconds": self.duration_seconds,
            "visibility": self.visibility.value,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "views": self.view_count
        }

    def __repr__(self) -> str:
        return (
            f"<{self.get_video_type()} | "
            f"id={self.video_id} | "
            f"title='{self.title}' | "
            f"status={self.status.value}>"
        )

    @abstractmethod
    def get_video_type(self) -> str:
        pass

    @abstractmethod
    def validate_specific_rules(self) -> bool:
        pass

