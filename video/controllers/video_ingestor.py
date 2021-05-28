import logging
import threading

from django.db import IntegrityError

from video.models import Video


class VideoIngestor:

    @staticmethod
    def if_already_present(video_id: str) -> bool:
        """Check if the video already exists in the database."""
        return Video.objects.filter(video_id=video_id).exists()

    def validate_and_insert(self, video_details: dict):
        """
        Insert the video into the model.

        :param video_details: dict
        {
          "kind": "youtube#searchResult",
          "etag": "3jMLLeDc016h7SxonFdRhSQ6GM0",
          "id": {
            "kind": "youtube#video",
            "videoId": "eY9dXcjkVx8"
          },
          "snippet": {
            "publishedAt": "2021-05-19T13:01:25Z",
            "channelId": "UCBJycsmduvYEL83R_U4JriQ",
            "title": "iPad Pro M1 Review: The Ultimate Spec Bump!",
            "description": "The M1 iPad Pro is unreal fast... at all the same stuff. Bring on iOS15! iPad Pro skins: http://dbrand.com/ipad MKBHD Merch: http://shop.MKBHD.com Tech I'm ...",
            "thumbnails": {
              "default": {
                "url": "https://i.ytimg.com/vi/eY9dXcjkVx8/default.jpg",
                "width": 120,
                "height": 90
              },
              "medium": {
                "url": "https://i.ytimg.com/vi/eY9dXcjkVx8/mqdefault.jpg",
                "width": 320,
                "height": 180
              },
              "high": {
                "url": "https://i.ytimg.com/vi/eY9dXcjkVx8/hqdefault.jpg",
                "width": 480,
                "height": 360
              }
            },
            "channelTitle": "Marques Brownlee",
            "liveBroadcastContent": "none",
            "publishTime": "2021-05-19T13:01:25Z"
          }
        }
        """
        video_id = video_details.get('id', {}).get('videoId')

        if not video_id or self.if_already_present(video_id):
            return

        try:
            Video.objects.create(
                etag=video_details['etag'],
                video_id=video_id,
                thumbnails=video_details['snippet']['thumbnails'],
                title=video_details['snippet']['title'],
                description=video_details['snippet']['description'],
                published_at=video_details['snippet']['publishTime']
            )
        except (AttributeError, IntegrityError, ValueError):
            return

    def ingest(self, items: list):
        """
        Ingests all the videos in the model.

        Validate if video is present inside model or not and then store it.

        :param items: list
            The list of video.
        :return: NoneType
        """
        threads = list()

        for index, item in enumerate(items):
            logging.info(f"{self.__class__.__name__}    : create and start thread {index}.")
            x = threading.Thread(target=self.validate_and_insert, args=(index,))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            logging.info(f"{self.__class__.__name__}    : before joining thread {index}.")
            thread.join()
            logging.info(f"{self.__class__.__name__}    : thread {index} done")
