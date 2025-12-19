from abc import ABC, abstractmethod
from enum import Enum
from uuid import uuid4
from datetime import datetime
from typing import Optional


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
    def __init__(
        self,
        channel_id: str,
        title: str,
        duration_seconds: int,
        visibility: VideoVisibility = VideoVisibility.PUBLIC
    ):
        self.video_id = str(uuid4())
        self.channel_id = channel_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.visibility = visibility
        self.status = VideoStatus.UPLOADED
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.last_watched_at: Optional[datetime] = None
        self.has_subtitles = False
        self.tags: list[str] = []

    def validate_duration(self) -> bool:
        return self.duration_seconds > 0

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        if tag in self.tags:
            self.tags.remove(tag)

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

    def mark_watched(self) -> None:
        self.last_watched_at = datetime.now()

    def enable_subtitles(self) -> None:
        self.has_subtitles = True

    def disable_subtitles(self) -> None:
        self.has_subtitles = False

    def change_visibility(self, visibility: VideoVisibility) -> None:
        self.visibility = visibility
        self.updated_at = datetime.now()

    def is_public(self) -> bool:
        return self.visibility == VideoVisibility.PUBLIC

    def is_blocked(self) -> bool:
        return self.status == VideoStatus.BLOCKED

    def is_published(self) -> bool:
        return self.status == VideoStatus.PUBLISHED

    def is_processing(self) -> bool:
        return self.status == VideoStatus.PROCESSING

    def is_uploaded(self) -> bool:
        return self.status == VideoStatus.UPLOADED

    def age_in_seconds(self) -> int:
        return int((datetime.now() - self.created_at).total_seconds())

    @abstractmethod
    def get_video_type(self) -> str:
        ...

    @abstractmethod
    def validate_specific_rules(self) -> bool:
        ...

    def is_valid(self) -> bool:
        return self.validate_duration() and self.validate_specific_rules()

    def __repr__(self) -> str:
        return (
            f"<{self.get_video_type()} "
            f"id={self.video_id} "
            f"title='{self.title}' "
            f"status={self.status.value} "
            f"visibility={self.visibility.value}>"
        )
