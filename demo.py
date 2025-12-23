from datetime import datetime, timedelta
from random import randint

from repository import VideoRepository
from services import VideoService
from implementations import StandardVideo, ShortVideo, LiveStreamVideo
from base import VideoVisibility, VideoStatus


def print_header(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


def print_videos(videos):
    for v in videos:
        print(v)


def create_standard_videos(service, count):
    videos = []
    for i in range(count):
        
        v = StandardVideo(
           channel_id="std_channel",
           title=f"Standard Video {i}",
           duration_seconds=600 + i * 10,
           has_subtitles=i % 2 == 0,
           visibility=VideoVisibility.PUBLIC
        )

        service.upload_video(v)
        
        if i % 2 == 0:
           service.process_and_publish(v.video_id)

        videos.append(v)

    return videos


def create_short_videos(service, count):
    videos = []
    for i in range(count):
       
        v = ShortVideo(
           channel_id="short_channel",
           title=f"Short Video {i}",
           duration_seconds=randint(10, 60),
           music_used=i % 3 == 0,
           visibility=VideoVisibility.PUBLIC
        )

        service.upload_video(v)
        service.process_and_publish(v.video_id)
        
        videos.append(v)

    return videos


def create_live_videos(service, count):
    videos = []
    for i in range(count):
       
        v = LiveStreamVideo(
           channel_id="live_channel",
           title=f"Live Stream {i}",
           scheduled_time=datetime.now() + timedelta(hours=i),
           visibility=VideoVisibility.PUBLIC
        )

        service.upload_video(v)
        if i % 2 == 0:
            v.start_stream()

        videos.append(v)

    return videos


def simulate_watching(service, videos):
    for v in videos:
        if v.status == VideoStatus.PUBLISHED:
            service.mark_video_watched(v.video_id)


def simulate_visibility_changes(service, videos):
    for i, v in enumerate(videos):
        if i % 3 == 0:
            service.change_visibility(v.video_id, VideoVisibility.PRIVATE)
        elif i % 3 == 1:
            service.change_visibility(v.video_id, VideoVisibility.UNLISTED)


def simulate_blocking(service, videos):
    for i, v in enumerate(videos):
        if i % 5 == 0:
            service.block_video(v.video_id)


def main():
    repository = VideoRepository()
    service = VideoService(repository)

    print_header("STANDARD VIDEOS CREATED")
    standard_videos = create_standard_videos(service, 10)
    print_videos(standard_videos)

    print_header("SHORT VIDEOS CREATED")
    short_videos = create_short_videos(service, 12)
    print_videos(short_videos)

    print_header("LIVE STREAMS CREATED")
    live_videos = create_live_videos(service, 6)
    print_videos(live_videos)

    print_header("SIMULATE WATCHING")
    simulate_watching(service, standard_videos)
    simulate_watching(service, short_videos)

    print_header("CHANGE VISIBILITY")
    simulate_visibility_changes(service, standard_videos)
    simulate_visibility_changes(service, short_videos)

    print_header("BLOCK SOME VIDEOS")
    simulate_blocking(service, short_videos)

    print_header("ALL VIDEOS")
    print_videos(service.list_all())

    print_header("PUBLIC VIDEOS")
    print_videos(service.list_public())

    print_header("BLOCKED VIDEOS")
    print_videos(service.list_blocked())

    print_header("PROCESSING VIDEOS")
    print_videos(service.list_processing())

    print_header("PUBLISHED VIDEOS")
    print_videos(service.list_by_status(VideoStatus.PUBLISHED))

    print_header("VIDEOS BY CHANNEL: std_channel")
    print_videos(service.list_by_channel("std_channel"))

    print_header("VIDEOS BY CHANNEL: short_channel")
    print_videos(service.list_by_channel("short_channel"))

    start = datetime.now() - timedelta(days=1)
    end = datetime.now() + timedelta(days=1)

    print_header("VIDEOS UPLOADED TODAY")
    print_videos(service.list_uploaded_between(start, end))

    print_header("SORTED BY TITLE")
    print_videos(service.sort_by_title())

    print_header("SORTED BY CREATED DATE DESC")
    print_videos(service.sort_by_created(reverse=True))

    print_header("PAGINATION PAGE 1 SIZE 5")
    print_videos(service.paginate(1, 5))

    print_header("PAGINATION PAGE 2 SIZE 5")
    print_videos(service.paginate(2, 5))

    print_header("CHANNEL LIST")
    print(service.channels())

    print_header("STATUS LIST")
    print(service.statuses())

    print_header("VISIBILITY LIST")
    print(service.visibilities())

    for v in standard_videos:
        service.add_tag(v.video_id, "education")
        service.add_tag(v.video_id, "python")

    for v in short_videos:
        service.add_tag(v.video_id, "shorts")

    print_header("VIDEOS AFTER TAGGING")
    print_videos(service.list_all())

    for v in standard_videos:
        if v.status == VideoStatus.PUBLISHED:
            service.unpublish_video(v.video_id)

    print_header("AFTER UNPUBLISH")
    print_videos(service.list_processing())


if __name__ == "__main__":
    main()
