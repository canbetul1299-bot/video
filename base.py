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
        self.flags: list[str] = []
        self.view_count = 0
        self.watch_time_seconds = 0
        self.rating_total = 0
        self.rating_count = 0
        self.metadata: dict[str, str] = {}

    def validate_duration(self) -> bool:
        return self.duration_seconds > 0

    def validate_title(self) -> bool:
        return bool(self.title and self.title.strip())

    def validate_channel(self) -> bool:
        return bool(self.channel_id and self.channel_id.strip())

    def is_valid(self) -> bool:
        return (
            self.validate_duration()
            and self.validate_title()
            and self.validate_channel()
            and self.validate_specific_rules()
        )

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

    def mark_watched(self, seconds: int = 0) -> None:
        self.last_watched_at = datetime.now()
        self.view_count += 1
        if seconds > 0:
            self.watch_time_seconds += seconds

    def enable_subtitles(self) -> None:
        self.has_subtitles = True

    def disable_subtitles(self) -> None:
        self.has_subtitles = False

    def add_tag(self, tag: str) -> None:
        if tag and tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        if tag in self.tags:
            self.tags.remove(tag)

    def clear_tags(self) -> None:
        self.tags.clear()

    def add_flag(self, flag: str) -> None:
        if flag and flag not in self.flags:
            self.flags.append(flag)

    def remove_flag(self, flag: str) -> None:
        if flag in self.flags:
            self.flags.remove(flag)

    def is_flagged(self) -> bool:
        return len(self.flags) > 0

    def add_rating(self, rating: int) -> None:
        if 1 <= rating <= 5:
            self.rating_total += rating
            self.rating_count += 1

    def average_rating(self) -> float:
        if self.rating_count == 0:
            return 0.0
        return self.rating_total / self.rating_count

    def set_metadata(self, key: str, value: str) -> None:
        if key:
            self.metadata[key] = value

    def get_metadata(self, key: str) -> Optional[str]:
        return self.metadata.get(key)

    def remove_metadata(self, key: str) -> None:
        if key in self.metadata:
            del self.metadata[key]

    def clear_metadata(self) -> None:
        self.metadata.clear()

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

    def age_seconds(self) -> int:
        return int((datetime.now() - self.created_at).total_seconds())

    def update_title(self, title: str) -> None:
        if title and title.strip():
            self.title = title
            self.updated_at = datetime.now()

    def update_duration(self, duration_seconds: int) -> None:
        if duration_seconds > 0:
            self.duration_seconds = duration_seconds
            self.updated_at = datetime.now()

    def can_be_recommended(self) -> bool:
        return (
            self.is_published()
            and not self.is_blocked()
            and self.average_rating() >= 3
        )

    def engagement_score(self) -> int:
        return self.view_count + len(self.tags) * 2 + len(self.flags) * -3

    def reset_statistics(self) -> None:
        self.view_count = 0
        self.watch_time_seconds = 0
        self.rating_total = 0
        self.rating_count = 0

    @abstractmethod
    def get_video_type(self) -> str:
        ...

    @abstractmethod
    def validate_specific_rules(self) -> bool:
        ...

    def __repr__(self) -> str:
        return (
            f"<{self.get_video_type()} "
            f"id={self.video_id} "
            f"title='{self.title}' "
            f"status={self.status.value} "
            f"visibility={self.visibility.value} "
            f"views={self.view_count}>"
        )
