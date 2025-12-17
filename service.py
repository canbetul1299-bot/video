
from datetime import datetime
from typing import List

from video.base import VideoBase, VideoStatus, VideoVisibility
from video.repository import VideoRepository


class VideoService: # Veri yönetme ve kuralları içerir.

    def __init__(self, repository: VideoRepository):
        self.repository = repository

   
    def upload_video(self, video: VideoBase) -> None: # Video yükler.
      
        if not video.validate_duration():
            raise ValueError("Video süresi geçersiz")

        self.repository.save(video)

    def start_processing(self, video_id: str) -> None: # Video process durumuna geçer.
      
        video = self._get_video_or_raise(video_id)
        video.process()

    def publish_video(self, video_id: str) -> None: # Video publish durumuna geçer.
        
        video = self._get_video_or_raise(video_id)

        if video.status != VideoStatus.PROCESSING:
            raise RuntimeError("Video processing durumunda değil")

        video.publish()

    def process_and_publish(self, video_id: str) -> None: # Process - publish geçişini gösterir.
       
        video = self._get_video_or_raise(video_id)
        video.process()
        video.publish()

    def unpublish_video(self, video_id: str) -> None: # Videoyu kaldırır.
        
        video = self._get_video_or_raise(video_id)
        video.unpublish()

    def block_video(self, video_id: str) -> None: # Videoyu engeller.
        
        video = self._get_video_or_raise(video_id)
        video.block()
    
    def list_videos_by_channel(self, channel_id: str) -> List[VideoBase]: # Kanaldaki video listeleme.
        
        return self.repository.find_by_channel(channel_id)

    def list_public_videos(self) -> List[VideoBase]: # Public video listeleme.
       
        return self.repository.find_public_videos()