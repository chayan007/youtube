import uuid as uuid
from django.db import models


class AbstractBaseModel(models.Model):
    """
    Base model for Youtube infrastructure.

    PS: Defined here to reduce file complexity.
    """
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created At', db_index=True
    )
    modified_at = models.DateTimeField(
        auto_now=True, verbose_name='Last Modified At'
    )
    is_deleted = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        """Define meta params for model."""

        abstract = True
        ordering = ('-created_at', )


class Video(AbstractBaseModel):
    """Video model to store all youtube videos."""

    etag = models.CharField(max_length=255)
    video_id = models.CharField(max_length=255, unique=True, db_index=True)
    thumbnails = models.JSONField(null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField()

    def __str__(self):
        return self.title
