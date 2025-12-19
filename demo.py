

from datetime import datetime, timedelta

from video.repository import VideoRepository
from video.services import VideoService
from video.implementations import StandardVideo, ShortVideo, LiveStreamVideo
from video.base import VideoVisibility, VideoStatus


def print_videos(title, videos):
    print("\n" + title)
    for v in videos:
        print(v)


def main():
    repository = VideoRepository()
    service = VideoService(repository)

    video1 = StandardVideo(
        channel_id="channel_1",
        title="Python OOP Dersleri",
        duration_seconds=900,
        has_subtitles=True
    )

    video2 = ShortVideo(
        channel_id="channel_1",
        title="Python İpucu",
        duration_seconds=45,
        music_used=True
    )

    video3 = LiveStreamVideo(
        channel_id="channel_2",
        title="Canlı Python Yayını",
        scheduled_time=datetime.now() + timedelta(hours=1)
    )

    service.upload_video(video1)
    service.upload_video(video2)
    service.upload_video(video3)

    service.process_and_publish(video1.video_id)
    service.process_and_publish(video2.video_id)

    video3.start_stream()
    video3.increase_viewers(120)
    video3.disable_chat()

    service.add_tag(video1.video_id, "python")
    service.add_tag(video1.video_id, "oop")
    service.add_tag(video2.video_id, "shorts")

    service.mark_video_watched(video1.video_id)
    service.mark_video_watched(video2.video_id)

    print_videos("Tum Videolar", service.list_all())
    print_videos("Public Videolar", service.list_public())
    print_videos("Yayindaki Videolar", service.list_by_status(VideoStatus.PUBLISHED))
    print_videos("Channel 1 Videolari", service.list_by_channel("channel_1"))

    start = datetime.now() - timedelta(days=1)
    end = datetime.now() + timedelta(days=1)

    print_videos(
        "Bugun Yuklenen Videolar",
        service.list_uploaded_between(start, end)
    )

    service.block_video(video2.video_id)

    print_videos(
        "Engellenmis Videolar",
        service.list_blocked()
    )

    service.change_visibility(video1.video_id, VideoVisibility.PRIVATE)

    print_videos(
        "Private Videolar",
        service.list_by_visibility(VideoVisibility.PRIVATE)
    )

    paged = service.paginate(page=1, page_size=2)
    print_videos("Sayfalama Sonucu", paged)

    sorted_by_title = service.sort_by_title()
    print_videos("Basliga Gore Sirali", sorted_by_title)

    service.unpublish_video(video1.video_id)

    print_videos(
        "Processing Durumundaki Videolar",
        service.list_processing()
    )


if __name__ == "__main__":
    main()