from celery import shared_task
from celery.utils.log import get_task_logger

from video.controllers.video_ingestor import VideoIngestor
from video.service import YoutubeService

logger = get_task_logger(__name__)


@shared_task(name='fetch_youtube_videos')
def fetch_youtube_videos():
    YoutubeService().fetch()


@shared_task(name='store_youtube_videos')
def store_youtube_videos(video_items: list):
    VideoIngestor().ingest(video_items)
