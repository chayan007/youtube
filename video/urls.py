from django.urls import path, include

from video.views import VideoSearchView


urlpatterns = [
    # Class Based Views
    path('v1/', include([
        path('', VideoSearchView.as_view(), name='search'),
    ])),
]
