from datetime import datetime
from typing import List, Optional

from video.base import VideoBase, VideoStatus, VideoVisibility
from video.repository import VideoRepository


class VideoService:
    def __init__(self, repository: VideoRepository):
        self.repository = repository

    def upload_video(self, video: VideoBase) -> None:
        if not video.is_valid():
            raise ValueError("Geçersiz video")
        self.repository.save(video)

    def start_processing(self, video_id: str) -> None:
        video = self._get(video_id)
        if video.status != VideoStatus.UPLOADED:
            raise RuntimeError("Geçersiz state")
        video.process()

    def publish_video(self, video_id: str) -> None:
        video = self._get(video_id)
        if video.status != VideoStatus.PROCESSING:
            raise RuntimeError("Geçersiz state")
        video.publish()

    def process_and_publish(self, video_id: str) -> None:
        video = self._get(video_id)
        if video.status == VideoStatus.UPLOADED:
            video.process()
        if video.status == VideoStatus.PROCESSING:
            video.publish()

    def unpublish_video(self, video_id: str) -> None:
        video = self._get(video_id)
        if video.status != VideoStatus.PUBLISHED:
            raise RuntimeError("Geçersiz state")
        video.unpublish()

    def block_video(self, video_id: str) -> None:
        video = self._get(video_id)
        video.block()

    def change_visibility(
        self,
        video_id: str,
        visibility: VideoVisibility
    ) -> None:
        video = self._get(video_id)
        video.change_visibility(visibility)

    def mark_video_watched(self, video_id: str) -> None:
        video = self._get(video_id)
        if video.status == VideoStatus.PUBLISHED:
            video.mark_watched()

    def enable_subtitles(self, video_id: str) -> None:
        video = self._get(video_id)
        video.enable_subtitles()

    def disable_subtitles(self, video_id: str) -> None:
        video = self._get(video_id)
        video.disable_subtitles()

    def add_tag(self, video_id: str, tag: str) -> None:
        video = self._get(video_id)
        video.add_tag(tag)

    def remove_tag(self, video_id: str, tag: str) -> None:
        video = self._get(video_id)
        video.remove_tag(tag)

    def list_all(self) -> List[VideoBase]:
        return self.repository.find_all()

    def list_by_channel(self, channel_id: str) -> List[VideoBase]:
        return self.repository.find_by_channel(channel_id)

    def list_by_status(self, status: VideoStatus) -> List[VideoBase]:
        return self.repository.find_by_status(status)

    def list_by_visibility(
        self,
        visibility: VideoVisibility
    ) -> List[VideoBase]:
        return self.repository.find_by_visibility(visibility)

    def list_public(self) -> List[VideoBase]:
        return self.repository.find_public_videos()

    def list_uploaded_between(
        self,
        start: datetime,
        end: datetime
    ) -> List[VideoBase]:
        return self.repository.find_uploaded_between(start, end)

    def list_updated_between(
        self,
        start: datetime,
        end: datetime
    ) -> List[VideoBase]:
        return self.repository.find_updated_between(start, end)

    def list_published_public(
        self,
        channel_id: Optional[str] = None
    ) -> List[VideoBase]:
        return self.repository.filter(
            channel_id=channel_id,
            status=VideoStatus.PUBLISHED,
            visibility=VideoVisibility.PUBLIC
        )

    def list_processing(self) -> List[VideoBase]:
        return self.repository.find_by_status(VideoStatus.PROCESSING)

    def list_blocked(self) -> List[VideoBase]:
        return self.repository.find_by_status(VideoStatus.BLOCKED)

    def list_unlisted(self) -> List[VideoBase]:
        return self.repository.find_by_visibility(VideoVisibility.UNLISTED)

    def any_blocked(self) -> bool:
        return self.repository.any_blocked()

    def any_published(self) -> bool:
        return self.repository.any_published()

    def remove_video(self, video_id: str) -> bool:
        return self.repository.remove(video_id)

    def paginate(
        self,
        page: int,
        page_size: int
    ) -> List[VideoBase]:
        return self.repository.paginate(page, page_size)

    def sort_by_created(self, reverse: bool = False) -> List[VideoBase]:
        return self.repository.sort_by_created(reverse)

    def sort_by_updated(self, reverse: bool = False) -> List[VideoBase]:
        return self.repository.sort_by_updated(reverse)

    def sort_by_title(self) -> List[VideoBase]:
        return self.repository.sort_by_title()

    def channels(self) -> set[str]:
        return self.repository.channels()

    def statuses(self) -> set[VideoStatus]:
        return self.repository.statuses()

    def visibilities(self) -> set[VideoVisibility]:
        return self.repository.visibilities()

    def _get(self, video_id: str) -> VideoBase:
        video = self.repository.find_by_id(video_id)
        if not video:
            raise LookupError("Video yok")
        return video