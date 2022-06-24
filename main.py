from datetime import datetime
import pandas as pd
from transform import clean_regions
from extract import *
from load import load


def extract_channels(channel_list, yt, date):
    # Prepare the dataframe where the channels' data will be stored
    columns = ['channelId', 'channelName', 'creationDate', 'country', 'viewCount', 'subscriberCount',
               'videoCount', 'extractionDate']

    df = pd.DataFrame(columns=columns)

    # Convert the channel list set into a list of 50 sized batches
    # This is done because the channel list supports a maximum of 50 results per query
    channel_list = [list(channel_list)[i:i + 50] for i in range(0, len(channel_list), 50)]

    # Update the "channels" dictionary with the cleaned information of every batch
    for batch in channel_list:
        ids = ','.join(batch)
        df = df.append(get_channels(ids, yt, columns, date), ignore_index=True)

    return df


def extract_videos(codes, yt, date):
    # Prepare the dataframe where the videos' data will be stored
    columns = ['videoId', 'videoTitle', 'publishedDate', 'channelId', 'viewCount', 'likeCount', 'commentCount',
               'language', 'trendedRegion', 'extractionDate']

    videos = pd.DataFrame(columns=columns)
    channel_list = set()

    # Fetch all the videos from each region and their information
    # The get_videos function already performs the cleaning process
    for region in codes:
        temp, regional_channels = get_videos(region, yt, columns, date)
        videos = videos.append(temp, ignore_index=True)
        channel_list |= regional_channels

    return videos, channel_list


def extract_regions(yt):
    # Get and clean all the regions
    raw_regions = get_regions(yt)
    cleaned = clean_regions(raw_regions)

    return cleaned


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    youtube = get_authenticated_service()

    # Perform the extraction process
    regions = extract_regions(youtube)
    videoData, channelList = extract_videos(regions['regionCode'], youtube, now)
    channels = extract_channels(channelList, youtube, now)

    # Perform the load phase
    load(regions, videoData, channels, now)
