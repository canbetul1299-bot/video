
import unittest
from datetime import datetime, timedelta

from base import VideoStatus, VideoVisibility
from implementations import (
    StandardVideo,
    ShortVideo,
    LiveStreamVideo
)
from repository import VideoRepository
from services import VideoService


class TestVideoCreation(unittest.TestCase):
    

    def setUp(self):
        self.repo = VideoRepository()
        self.service = VideoService(self.repo)

    def test_standard_video_upload(self):
        video = StandardVideo(
            channel_id="channel_1",
            title="Test Video",
            duration_seconds=300
        )

        self.service.upload_video(video)

        self.assertEqual(self.repo.count(), 1)
        self.assertEqual(video.status, VideoStatus.UPLOADED)

    def test_invalid_short_video_duration(self):
        video = ShortVideo(
            channel_id="channel_1",
            title="Geçersiz Short",
            duration_seconds=120
        )

        with self.assertRaises(ValueError):
            self.service.upload_video(video)


class TestStatusTransitions(unittest.TestCase):


    def setUp(self):
        self.repo = VideoRepository()
        self.service = VideoService(self.repo)

        self.video = StandardVideo(
            channel_id="channel_1",
            title="Durum Testi",
            duration_seconds=200
        )
        self.service.upload_video(self.video)

    def test_processing_to_published(self):
        self.service.start_processing(self.video.video_id)
        self.assertEqual(self.video.status, VideoStatus.PROCESSING)

        self.service.publish_video(self.video.video_id)
        self.assertEqual(self.video.status, VideoStatus.PUBLISHED)

    def test_process_and_publish(self):
        self.service.process_and_publish(self.video.video_id)
        self.assertEqual(self.video.status, VideoStatus.PUBLISHED)


class TestBlockingAndUnpublish(unittest.TestCase):
    
    
    def setUp(self):
        self.repo = VideoRepository()
        self.service = VideoService(self.repo)

        self.video = StandardVideo(
            channel_id="channel_2",
            title="Engelleme Testi",
            duration_seconds=400
        )
        self.service.upload_video(self.video)
        self.service.process_and_publish(self.video.video_id)

    def test_block_video(self):
        self.service.block_video(self.video.video_id)
        self.assertEqual(self.video.status, VideoStatus.BLOCKED)

    def test_unpublish_video(self):
        self.service.unpublish_video(self.video.video_id)
        self.assertEqual(self.video.status, VideoStatus.PROCESSING)


class TestRepositoryFilters(unittest.TestCase):
    
    def setUp(self):
        self.repo = VideoRepository()

        self.v1 = StandardVideo(
            channel_id="channel_1",
            title="Video 1",
            duration_seconds=300
        )

        self.v2 = ShortVideo(
            channel_id="channel_1",
            title="Video 2",
            duration_seconds=40,
            visibility=VideoVisibility.PRIVATE
        )

        self.v3 = LiveStreamVideo(
            channel_id="channel_2",
            title="Video 3"
        )

        self.repo.save(self.v1)
        self.repo.save(self.v2)
        self.repo.save(self.v3)

    def test_find_by_channel(self):
        videos = self.repo.find_by_channel("channel_1")
        self.assertEqual(len(videos), 2)

    def test_find_by_visibility(self):
        public_videos = self.repo.find_by_visibility(VideoVisibility.PUBLIC)
        self.assertEqual(len(public_videos), 2)

    def test_find_by_status(self):
        blocked = self.repo.find_by_status(VideoStatus.BLOCKED)
        self.assertEqual(len(blocked), 0)

    def test_date_range_filter(self):
        start = datetime.now() - timedelta(days=1)
        end = datetime.now() + timedelta(days=1)

        videos = self.repo.find_uploaded_between(start, end)
        self.assertEqual(len(videos), 3)


if __name__ == "__main__":
    unittest.main()