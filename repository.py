from datetime import datetime
from typing import List, Optional, Dict
from collections import defaultdict

from video.base import VideoBase, VideoStatus, VideoVisibility


class VideoRepository:
    def __init__(self):
        self._videos: Dict[str, VideoBase] = {}

    def save(self, video: VideoBase) -> None:
        self._videos[video.video_id] = video

    def remove(self, video_id: str) -> bool:
        if video_id in self._videos:
            del self._videos[video_id]
            return True
        return False

    def count(self) -> int:
        return len(self._videos)

    def exists(self, video_id: str) -> bool:
        return video_id in self._videos

    def find_all(self) -> List[VideoBase]:
        return list(self._videos.values())

    def find_by_id(self, video_id: str) -> Optional[VideoBase]:
        return self._videos.get(video_id)

    def find_by_channel(self, channel_id: str) -> List[VideoBase]:
        return [
            v for v in self._videos.values()
            if v.channel_id == channel_id
        ]

    def find_by_status(self, status: VideoStatus) -> List[VideoBase]:
        return [
            v for v in self._videos.values()
            if v.status == status
        ]

    def find_by_visibility(self, visibility: VideoVisibility) -> List[VideoBase]:
        return [
            v for v in self._videos.values()
            if v.visibility == visibility
        ]

    def find_public_videos(self) -> List[VideoBase]:
        return [
            v for v in self._videos.values()
            if v.visibility == VideoVisibility.PUBLIC
        ]

    def find_uploaded_between(
        self,
        start: datetime,
        end: datetime
    ) -> List[VideoBase]:
        return [
            v for v in self._videos.values()
            if start <= v.created_at <= end
        ]

    def find_updated_between(
        self,
        start: datetime,
        end: datetime
    ) -> List[VideoBase]:
        return [
            v for v in self._videos.values()
            if v.updated_at and start <= v.updated_at <= end
        ]

    def filter(
        self,
        channel_id: Optional[str] = None,
        status: Optional[VideoStatus] = None,
        visibility: Optional[VideoVisibility] = None
    ) -> List[VideoBase]:
        result = list(self._videos.values())

        if channel_id is not None:
            result = [v for v in result if v.channel_id == channel_id]

        if status is not None:
            result = [v for v in result if v.status == status]

        if visibility is not None:
            result = [v for v in result if v.visibility == visibility]

        return result

    def paginate(
        self,
        page: int,
        page_size: int
    ) -> List[VideoBase]:
        if page < 1 or page_size < 1:
            return []

        start = (page - 1) * page_size
        end = start + page_size

        return list(self._videos.values())[start:end]

    def sort_by_title(self) -> List[VideoBase]:
        return sorted(
            self._videos.values(),
            key=lambda v: v.title.lower()
        )

    def sort_by_created(self, reverse: bool = False) -> List[VideoBase]:
        return sorted(
            self._videos.values(),
            key=lambda v: v.created_at,
            reverse=reverse
        )

    def sort_by_updated(self, reverse: bool = False) -> List[VideoBase]:
        return sorted(
            self._videos.values(),
            key=lambda v: v.updated_at or v.created_at,
            reverse=reverse
        )

    def any_blocked(self) -> bool:
        return any(
            v.status == VideoStatus.BLOCKED
            for v in self._videos.values()
        )

    def any_published(self) -> bool:
        return any(
            v.status == VideoStatus.PUBLISHED
            for v in self._videos.values()
        )

    def channels(self) -> set:
        return {v.channel_id for v in self._videos.values()}

    def statuses(self) -> set:
        return {v.status for v in self._videos.values()}

    def visibilities(self) -> set:
        return {v.visibility for v in self._videos.values()}

    def count_by_channel(self) -> Dict[str, int]:
        result = defaultdict(int)
        for v in self._videos.values():
            result[v.channel_id] += 1
        return dict(result)

    def count_by_status(self) -> Dict[VideoStatus, int]:
        result = defaultdict(int)
        for v in self._videos.values():
            result[v.status] += 1
        return dict(result)

    def count_by_visibility(self) -> Dict[VideoVisibility, int]:
        result = defaultdict(int)
        for v in self._videos.values():
            result[v.visibility] += 1
        return dict(result)

    def latest(self, limit: int = 5) -> List[VideoBase]:
        return sorted(
            self._videos.values(),
            key=lambda v: v.created_at,
            reverse=True
        )[:limit]

    def oldest(self, limit: int = 5) -> List[VideoBase]:
        return sorted(
            self._videos.values(),
            key=lambda v: v.created_at
        )[:limit]

    def clear(self) -> None:
        self._videos.clear()

    def __len__(self):
        return len(self._videos)

    def __iter__(self):
        return iter(self._videos.values())
