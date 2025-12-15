
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

    def find_by_channel(self, channel_id: str) -> List[VideoBase]: # Belirli bir kanaldaki tüm videoları listeler.
        
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

    def find_published(self) -> List[VideoBase]: # Yayındaki videoları listeler.
     
        return self.find_by_status(VideoStatus.PUBLISHED)

    def find_blocked(self) -> List[VideoBase]: # Engellenmiş videoları listeler.
        
        return self.find_by_status(VideoStatus.BLOCKED)

    # VISIBILITY BAZLI FİLTRELER
    
    def find_by_visibility(
        self,
        visibility: VideoVisibility
    ) -> List[VideoBase]: # Görünürlük tipine göre video listelemesi yapar.
        
        return [
            video for video in self._videos
            if video.visibility == visibility
        ]
    def find_public_videos(self) -> List[VideoBase]: # Sadece public videoları çalıştırır.
    
        return self.find_by_visibility(VideoVisibility.PUBLIC)
    
    # TARİH BAZLI FİLTRELER

    def find_uploaded_after(self, date: datetime) -> List[VideoBase]: # Belirli bir tarihten sonra yüklenen videoları çalıştırır.
        
        return [
            video for video in self._videos
            if video.upload_date >= date
        ]
    def find_uploaded_between(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[VideoBase]: #  Tarihler arasında yüklenen videoları çalıştırır.
        
        return [
            video for video in self._videos
            if start_date <= video.upload_date <= end_date
        ]
    
    def filter(  # Filtreleme yapar.
        self,
        channel_id: Optional[str] = None,
        status: Optional[VideoStatus] = None,
        visibility: Optional[VideoVisibility] = None
    ) -> List[VideoBase]:
        
        result = self._videos

        if channel_id is not None:
            result = [
                v for v in result
                if v.channel_id == channel_id
            ]

        if status is not None:
            result = [
                v for v in result
                if v.status == status
            ]

        if visibility is not None:
            result = [
                v for v in result
                if v.visibility == visibility
            ]

        return result