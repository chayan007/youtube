from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from video.controllers.video_model_ops import VideoModelOps
from video.serializers import VideoSerializer


class VideoSearchView(GenericAPIView):

    serializer_class = VideoSerializer

    def get(self, request, *args, **kwargs):
        """Get all the matching video records."""
        search_string = request.query_params.get('search')
        video_ops = VideoModelOps()

        if not search_string:
            self.queryset = video_ops.get_all()
        else:
            self.queryset = video_ops.get_based_on_search(search_string)

        if not self.queryset:
            return Response(
                data={'error': f'No videos found for [{search_string}]'},
                status=status.HTTP_404_NOT_FOUND
            )

        paginator = PageNumberPagination()
        paginator.page_size = 50

        paginated_queryset = paginator.paginate_queryset(self.queryset, request)
        serialized_videos = self.serializer_class(paginated_queryset, many=True)

        return paginator.get_paginated_response(serialized_videos.data)
