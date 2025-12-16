from datetime import datetime
from typing import Optional, List

from Video.base import (
     VideoBase,
     VideoStatus,
     VideoVisibility
)

class StandardVideo(VideoBase): # Klasik, önceden kaydedilmiş videolar.

    def __init__(
        self,
        channel_id: str,
        title: str,
        duration_seconds: int,
        visibility: VideoVisibility,
        resolution: str = "1080p",
        has_subtitles: bool = False
    ):
        super().__init__(
            video_id=VideoBase.generate_video_id(),
            channel_id=channel_id,
            title=title,
            duration_seconds=duration_seconds,
            visibility=visibility,
            status=VideoStatus.uploaded
        )

        self.resolution = resolution
        self.has_subtitles = has_subtitles
        self.last_watched_at: Optional[datetime] = None

   

    def get_video_type(self) -> str:
        return "StandardVideo"

    def validate_duration(self) -> bool:
        return self.duration_seconds >= 10

   

    def mark_watched(self) -> None:
        self.last_watched_at = datetime.now()

    def enable_subtitles(self) -> None:
        self.has_subtitles = True

    def disable_subtitles(self) -> None:
        self.has_subtitles = False


class LiveStreamVideo(VideoBase): # Canlı yayın videoları.

    def __init__(
        self,
        channel_id: str,
        title: str,
        visibility: VideoVisibility,
        scheduled_time: Optional[datetime] = None
    ):
        super().__init__(
            video_id=VideoBase.generate_video_id(),
            channel_id=channel_id,
            title=title,
            duration_seconds=0,
            visibility=visibility,
            status=VideoStatus.uploaded
        )

        self.scheduled_time = scheduled_time
        self.is_live = False
        self.started_at: Optional[datetime] = None
        self.ended_at: Optional[datetime] = None

    
    def get_video_type(self) -> str:
        return "LiveStreamVideo"

    def validate_duration(self) -> bool:
        return True

    

    def start_stream(self) -> None:
        if not self.is_live:
            self.is_live = True
            self.started_at = datetime.now()
            self.status = VideoStatus.published

    def end_stream(self, final_duration: int) -> None:
        if self.is_live:
            self.is_live = False
            self.ended_at = datetime.now()
            self.duration_seconds = final_duration
            self.status = VideoStatus.processing

    def is_scheduled(self) -> bool:
        return self.scheduled_time is not None


class ShortVideo(VideoBase): # Shorts videolar.
    
    MAX_DURATION = 60

    def __init__(
        self,
        channel_id: str,
        title: str,
        duration_seconds: int,
        visibility: VideoVisibility,
        is_vertical: bool = True,
        music_used: bool = False
    ):
        super().__init__(
            video_id=VideoBase.generate_video_id(),
            channel_id=channel_id,
            title=title,
            duration_seconds=duration_seconds,
            visibility=visibility,
            status=VideoStatus.uploaded
        )

        self.is_vertical = is_vertical
        self.music_used = music_used
        self.loop_count = 0

   

    def get_video_type(self) -> str:
        return "ShortVideo"

    def validate_duration(self) -> bool:
        return 0 < self.duration_seconds <= self.MAX_DURATION

  

    def increment_loop(self) -> None:
        self.loop_count += 1

    def uses_music(self) -> bool:
        return self.music_used

    def is_valid_short(self) -> bool:
        return self.is_vertical and self.validate_duration()

    @staticmethod
    def validate_all_videos(videos: List[VideoBase]) -> List[VideoBase]:
        valid_videos = []
        for video in videos:
            if video.validate_duration():
                valid_videos.append(video)
        return valid_videos