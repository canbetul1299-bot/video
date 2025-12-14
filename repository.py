
from datetime import datetime
from typing import List, Optional

from video.base import VideoBase, VideoStatus, VideoVisibility


class VideoRepository: # VideoRepository, video nesnelerinin tutulduğu ve sorgulandığı katmandır.

    def __init__(self):
        self._videos: List[VideoBase] = []

    # CRUD BENZERİ METOTLAR
   
    def save(self, video: VideoBase) -> None: # Yeni bir video kaydeder.
        self._videos.append(video)

    def delete(self, video_id: str) -> bool: # Video ID'ye göre silme işlemi yapar.
       
        video = self.find_by_id(video_id)
        if video:
            self._videos.remove(video)
            return True
        return False

    def find_by_id(self, video_id: str) -> Optional[VideoBase]: # Video ID'ye göre tekil video bulur.
        
        for video in self._videos:
            if video.video_id == video_id:
                return video
        return None

    def find_all(self) -> List[VideoBase]: # Sistemdeki tüm videoları döndürür.
        
        return list(self._videos)

    # KANAL BAZLI FİLTRELER

    def find_by_channel(self, channel_id: str) -> List[VideoBase]: # Belirli bir kanala ait tüm videoları listeler.
        
        return [
            video for video in self._videos
            if video.channel_id == channel_id
        ]

    # STATUS BAZLI FİLTRELER

    def find_by_status(self, status: VideoStatus) -> List[VideoBase]: # Belirli bir statüdeki videoları listeler.
        
        return [
            video for video in self._videos
            if video.status == status
        ]

    def find_published(self) -> List[VideoBase]: # Yayında olan videoları listeler.
     
        return self.find_by_status(VideoStatus.PUBLISHED)

    def find_blocked(self) -> List[VideoBase]: # Engellenmiş videoları listeler.
        
        return self.find_by_status(VideoStatus.BLOCKED)

    