

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
        title="Canli Python Yayini",
        scheduled_time=datetime.now() + timedelta(hours=2)
    )

    service.upload_video(standard_video)
    service.upload_video(short_video)
    service.upload_video(live_video)
    

    service.process_and_publish(standard_video.video_id)
    service.process_and_publish(short_video.video_id)

    live_video.start_stream()

    all_videos = repository.find_all()

    print_video_list(
        "Tüm Videolar (Polimorfik Liste)",
        all_videos
    )

    print_video_list(
        "Yayindaki Videolar",
        service.list_videos_by_status(VideoStatus.PUBLISHED)
    )

    print_video_list(
        "Public Videolar",
        service.list_public_videos()
    )

    print_video_list(
        "Channel 1 Videoları",
        service.list_videos_by_channel("channel_1")
    )


    start = datetime.now() - timedelta(days=1)
    end = datetime.now() + timedelta(days=1)

    print_video_list(
        "Bugün Yüklenen Videolar",
        service.list_videos_by_date_range(start, end)
    )

    service.block_video(short_video.video_id)

    print_video_list(
        "Engellenmiş Videolar",
        service.list_videos_by_status(VideoStatus.BLOCKED)
    )


if __name__ == "__main__":
    main()