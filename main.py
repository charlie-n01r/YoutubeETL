import os
import pickle
import json
import google_auth_oauthlib.flow
from googleapiclient import discovery
from transform import clean_regions, clean_video_list, clean_channels

scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']
api_service_name = 'youtube'
api_version = 'v3'
client_secrets_file = 'secrets.json'


def get_channels(ids, yt):
    request = yt.channels().list(
        part="snippet,statistics",
        id=ids
    )
    response = request.execute()

    return response


def get_videos(code, yt, data):
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
    video_list, channels = clean_video_list(response)
    data[code] = video_list

    return channels


def get_regions(yt):
    # Fetch all of YouTube's regions
    request = yt.i18nRegions().list(
        part="snippet"
    )
    response = request.execute()

    return response


def get_authenticated_service():
    if os.path.exists('credentials'):
        with open('credentials', 'rb') as f:
            credentials = pickle.load(f)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()
        with open('credentials', 'wb') as f:
            pickle.dump(credentials, f)
    return discovery.build(api_service_name, api_version, credentials=credentials)


if __name__ == '__main__':
    videoData = dict()
    channelList = set()

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    youtube = get_authenticated_service()
    
    raw_regions = get_regions(youtube)
    regions = clean_regions(raw_regions)
    test = list(regions.keys())[:2]

    for region in test:
        regional_channels = get_videos(region, youtube, videoData)
        channelList |= regional_channels

    with open('videos.json', 'w', encoding='utf-8') as file:
        json.dump(videoData, file, ensure_ascii=False, indent=2)

    channelIDs = ','.join(channelList)
    raw_channels = get_channels(channelIDs, youtube)
    channels = clean_channels(raw_channels)

    with open('channels.json', 'w', encoding='utf-8') as file:
        json.dump(channels, file, ensure_ascii=False, indent=2)