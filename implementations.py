from datetime import datetime
from typing import Optional

from video.base import (
    VideoBase,
    VideoStatus,
    VideoVisibility
)
class StandardVideo(VideoBase): # Klasik, önceden kaydedilmiş videoları temsil eder.
    
    def __init__(self, channel_id, title, duration_seconds, resolution = "1080p", has_subtitles = False, visibility):
        super().__init__(
            self.channel_id = channel_id,
            self.title = title,
            self.duration_seconds = duration_seconds,
            self.visibility = visibility
        )
        self.resolution = resolution
        self.has_subtitles = has_subtitles
        self.last_watched_at: Optional[datetime] = None

        # ========== ABSTRACT METHOD OVERRIDE ==========

    def get_video_type(self):
        return "StandardVideo"

    def validate_duration(self): # Standard videolar için süre en az 10 saniye olmalı.
        return self.duration_seconds >= 10

        # ========== KENDİNE ÖZGÜ METOTLAR ==========
    
    def mark_watched(self): # Videonun izlendiği zamanı kaydeder.
        self.last_watched_at = datetime.now()

    def enable_subtitles(self):
        self.has_subtitles = True

    def disable_subtitles(self):
        self.has_subtitles = False

class LiveStreamVideo(VideoBase): # Canlı yayın videolarını temsil eder.
  
    def __init__(self, channel_id, title, scheduled_time: Optional[datetime] = None, visibility):
        super().__init__(
            self.channel_id = channel_id,
            self.title = title,
            self.duration_seconds = 0,
            self.visibility = visibility
        )
        self.scheduled_time: Optional[datetime] = scheduled_time
        self.is_live = False
        self.started_at: Optional[datetime] = None
        self.ended_at: Optional[datetime] = None

 # ========== ABSTRACT METHOD OVERRIDE ==========

    def get_video_type(self):
        return "LiveStreamVideo"

    def validate_duration(self): # Canlı yayınlarda başlangıçta süre kontrolü yapılmaz.
        return True

    # ========== KENDİNE ÖZGÜ METOTLAR ==========

    def start_stream(self): # Canlı yayını başlatır.

        if not self.is_live:
               self.is_live = True
               self.started_at = datetime.now()
               self.status = VideoStatus.published

    def end_stream(self, final_duration): # Canlı yayını bitirir ve süreyi kaydeder.
    
        if self.is_live:
           self.is_live = False
           self.ended_at = datetime.now()
           self.duration_seconds = final_duration
           self.status = VideoStatus.processing

    def is_scheduled(self):
        return self.scheduled_time is not None # Canlı yayın planlanmış mı boolean kontrol yapar.

class ShortVideo(VideoBase): # Kısa, dikey formatlı videoları temsil eder (Shorts).
    
    MAX_DURATION = 60

    def __init__(self, channel_id, title, duration_seconds, is_vertical = True, music_used = False, visibility):
        super().__init__(
            self.channel_id = channel_id,
            self.title = title,
            self.duration_seconds = duration_seconds,
            self.visibility = visibility
        )
        self.is_vertical = is_vertical
        self.music_used: = music_used
        self.loop_count  = 0

    # ========== ABSTRACT METHOD OVERRIDE ==========

    def get_video_type(self):
        return "ShortVideo"

    def validate_duration(self): # Short videolar maksimum 60 saniye olabilir.
    
        return 0 < self.duration_seconds <= self.MAX_DURATION

    # ========== KENDİNE ÖZGÜ METOTLAR ==========

    def increment_loop(self): # Video her döngüye girdiğinde sayacı artırır.

        self.loop_count += 1

    def uses_music(self):
        return self.music_used

    def is_valid_short(self): # Hem süre hem format açısından short olup olmadığını kontrol eder.
        return self.is_vertical and self.validate_duration()

    def validate_all_videos(videos: list[VideoBase]) -> list[VideoBase]: # Farklı video türlerini tek listede alır,
                                                                         # abstract method'lar sayesinde polimorfik çalışır.
       valid_videos = []
       for video in videos:
            if video.validate_duration():
              valid_videos.append(video)
       return valid_videos