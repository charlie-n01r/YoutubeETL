import os
import pickle
import google_auth_oauthlib.flow
from googleapiclient import discovery
from transform import clean_video_list, clean_channels

scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']
api_service_name = 'youtube'
api_version = 'v3'
client_secrets_file = 'secrets.json'


def get_authenticated_service():
    # If there is a credentials file, then use it to authenticate
    if os.path.exists('credentials'):
        with open('credentials', 'rb') as f:
            credentials = pickle.load(f)
    else:
        # Otherwise, it will be necessary to get authenticated manually once
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()
        with open('credentials', 'wb') as f:
            pickle.dump(credentials, f)

    return discovery.build(api_service_name, api_version, credentials=credentials)


def get_channels(ids, yt, columns, date):
    # Get the statistics and other information from the channels whose video trended
    request = yt.channels().list(
        part="snippet,statistics",
        id=ids
    )
    response = request.execute()
    channel_info = clean_channels(response, columns, date)

    return channel_info


def get_videos(code, yt, columns, now):
    # Get the top 10 trending videos in Gaming in a given region
    request = yt.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        maxResults=10,
        regionCode=code,
        videoCategoryId="20"
    )
    response = request.execute()

    # Clean and store the information of each video
    videos, channels = clean_video_list(response, columns, now, code)

    return videos, channels


def get_regions(yt):
    # Fetch all of YouTube's regions
    request = yt.i18nRegions().list(
        part="snippet"
    )
    response = request.execute()

    return response
