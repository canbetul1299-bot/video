
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
