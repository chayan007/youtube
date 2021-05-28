from rest_framework import serializers

from video.models import Video


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = (
            'etag',
            'video_id',
            'thumbnails',
            'title',
            'description',
            'published_at'
        )
