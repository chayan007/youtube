from django.contrib.postgres.search import SearchVector

from video.models import Video


class VideoModelOps:

    @staticmethod
    def get_based_on_search(search_str: str) -> [Video]:
        return Video.objects.annotate(
            search=SearchVector('title', 'description'),
         ).filter(
            search=search_str
        )
