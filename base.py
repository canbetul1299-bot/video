from abc import ABC, abstractmethod  # Soyut sınıf ve soyut method
from datetime import datetime
import uuid

class VideoBase(ABC):
   
   VALID_VISIBILITIES = {"public", "private", "unlisted"}
   VALID_STATUSES = {"uploaded", "processing", "published", "blocked", "removed"}
   
  def __init__(self, video_id, channel_id, title, duration_seconds, visibility, status):
     
     self.video_id = video_id
     self.channel_id = channel_id
     self.title = title
     self.duration_seconds = duration_seconds
     self.visibility = visibility
     self.status = status
     self.upload_date: datetime = datetime.now()
     self.last_updated: datetime = datetime.now()


  def process(self):
        if self.status == "uploaded":
            self.status = "processing"

  def publish(self):
        if self.status == "processing":
            self.status = "published"

  def block(self):
        self.status = "blocked"
    
  def unpublish(self):
        if self.status == "published":
            self.status = "processing"
  
  def change_visibility(self, visibility: VideoVisibility): # Video görünürlüğünü değiştirir.
        self.visibility = visibility


 @abstractmethod
    def get_video_type(self):  # Metodu alt sınıflar yazsın
        pass

 @abstractmethod
    def validate_duration(self): #  Video süresinin alt sınıfa göre uygun olup olmadığını kontrol eder.
        pass
 
    def _touch(self): # Son güncelleme zamanını yeniler.
        self.last_updated = datetime.now()

    def is_public(self):
        return self.visibility == VideoVisibility.public

    def is_blocked(self):
        return self.status == VideoStatus.blocked

    def can_be_published(self):
        return self.status == VideoStatus.processing


    @classmethod
    def allowed_visibilities(cls): # Sistemde desteklenen görünürlük tiplerini döndürür.
        return [v.value for v in VideoVisibility]
    
    @staticmethod
    def generate_video_id(): # Harici kullanım için video ID üretir.
        return str(uuid.uuid4())
      
    def __repr__(self):  # Polimorfizm var: her subclass farklı döndürür.
        return (
            f"<{self.get_video_type()} | "
            f"id={self.video_id} | "
            f"title='{self.title}' | "
            f"status={self.status.value}>"
        )
 