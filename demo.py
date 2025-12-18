

from datetime import datetime, timedelta

from video.base import VideoVisibility, VideoStatus
from video.implementations import (
    StandardVideo,
    LiveStreamVideo,
    ShortVideo
)
from video.repository import VideoRepository
from video.services import VideoService


def print_video_list(title: str, videos: list):
    print(f"\n--- {title} ---")
    for video in videos:
        print(video)


def main():
   
    repository = VideoRepository()
    service = VideoService(repository)

    standard_video = StandardVideo(
        channel_id="channel_1",
        title="Python OOP Dersi",
        duration_seconds=900,
        has_subtitles=True
    )

    short_video = ShortVideo(
        channel_id="channel_1",
        title="Python Short İpucu",
        duration_seconds=45,
        music_used=True
    )

    live_video = LiveStreamVideo(
        channel_id="channel_2",
        title="Canlı Python Yayını",
        scheduled_time=datetime.now() + timedelta(hours=2)
    )

    service.upload_video(standard_video)
    service.upload_video(short_video)
    service.upload_video(live_video)
    

    service.process_and_publish(standard_video.video_id)
    service.process_and_publish(short_video.video_id)

    live_video.start_stream()
