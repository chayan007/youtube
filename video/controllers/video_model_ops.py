from django.contrib.postgres.search import SearchVector
from django.db.models import Q

from video.models import Video


class VideoModelOps:

    @staticmethod
    def get_based_on_search(search_str: str) -> [Video]:
        # return Video.objects.annotate(
        #     search=SearchVector('title', 'description'),
        #  ).filter(
        #     search=search_str
        # )
        return Video.objects.filter(
            Q(title__icontains=search_str) |
            Q(description__icontains=search_str)
        ).order_by('-published_at')
