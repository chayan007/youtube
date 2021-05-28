import datetime
import logging
import os

from django.conf import settings
from googleapiclient.discovery import build

import celery


class YoutubeService:

    def fetch(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        next_page_token = None
        num_of_yt_api_keys = len(settings.YOUTUBE_API_KEYS)
        current_yt_api_key_index = 0
        yt_api_key = settings.YOUTUBE_API_KEYS[current_yt_api_key_index]

        while True:
            try:
                youtube = build(
                    api_service_name,
                    api_version,
                    developerKey=yt_api_key
                )

                request = youtube.search().list(
                    part="snippet",
                    order="date",
                    publishedAfter=(
                        datetime.datetime.now() - datetime.timedelta(
                            # The aim was to take exactly same time (minute) frequency
                            # but as we are using data, thus we have to create such inconsistent
                            # retrieve parameter by going for a day old (not a minute old).
                            # PS: Tried with 1 minute difference, got empty data.
                            days=settings.TASK_FREQUENCY
                        )
                    ).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    type="video",
                    pageToken=next_page_token
                )
                response = request.execute()

                logging.info(f"{self.__class__.__name__}    : Pushing response into task queue.")
                celery.current_app.send_task('video.tasks.store_youtube_videos', (response.get('items'),))

                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    logging.info(f"{self.__class__.__name__}    : No more pages to continue flow.")
                    continue

            except BaseException as e:
                logging.info(f"{self.__class__.__name__}    : Current API Token Exhausted..")
                current_yt_api_key_index += 1

                if current_yt_api_key_index < num_of_yt_api_keys:
                    logging.info(f"{self.__class__.__name__}    : Using Token No. [{current_yt_api_key_index}]")
                    yt_api_key = settings.YOUTUBE_API_KEYS[current_yt_api_key_index]
                    continue

                logging.info(f"{self.__class__.__name__}    : No more API Token to continue flow.")
                return
