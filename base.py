from abc import ABC, abstractmethod
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
        self.upload_date = datetime.now()
        self.last_updated = datetime.now()

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

    def change_visibility(self, visibility):
        if visibility in self.VALID_VISIBILITIES:
            self.visibility = visibility

    @abstractmethod
    def get_video_type(self):
        pass

    @abstractmethod
    def validate_duration(self):
        pass

    def _touch(self):
        self.last_updated = datetime.now()

    def is_public(self):
        return self.visibility == "public"

    def is_blocked(self):
        return self.status == "blocked"

    def can_be_published(self):
        return self.status == "processing"

    @classmethod
    def allowed_visibilities(cls):
        return list(cls.VALID_VISIBILITIES)

    @staticmethod
    def generate_video_id():
        return str(uuid.uuid4())

    def __repr__(self):
        return (
            f"<{self.get_video_type()} | "
            f"id={self.video_id} | "
            f"title='{self.title}' | "
            f"status={self.status}>"
       )
<<<<<<< HEAD
 
=======
>>>>>>> 9ad9038e200d564e0cd5dd8f6245309373525ff4
