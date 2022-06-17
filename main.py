import os
import pickle
import json
import google_auth_oauthlib.flow
from googleapiclient import discovery
from transform import clean_regions

scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']
api_service_name = 'youtube'
api_version = 'v3'
client_secrets_file = 'secrets.json'


def get_channel(ids, yt):
    request = yt.channels().list(
        part="snippet,statistics",
        id=ids
    )
    response = request.execute()
    with open('channels.json', 'w', encoding='utf-8') as file:
        json.dump(response, file, ensure_ascii=False, indent=2)


def get_videos(code, yt):
    request = yt.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        maxResults=15,
        regionCode=code,
        videoCategoryId="20"
    )
    response = request.execute()
    with open('videos.json', 'w', encoding='utf-8') as file:
        json.dump(response, file, ensure_ascii=False, indent=2)


def get_regions(yt):
    request = yt.i18nRegions().list(
        part="snippet"
    )
    response = request.execute()

    return response


# def get_search(yt, region):
#     request = yt.search().list(
#         part='snippet',
#         maxResults=15,
#         q='asmr',
#         regionCode=region,
#         type='video'
#     )
#     response = request.execute()
#     with open('results.json', 'a', encoding='utf-8') as file:
#         json.dump(response, file, ensure_ascii=False, indent=2)


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
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    youtube = get_authenticated_service()
    
    raw_regions = get_regions(youtube)
    regions = clean_regions(raw_regions)

    for region in regions.keys():
        get_videos(region, youtube)
