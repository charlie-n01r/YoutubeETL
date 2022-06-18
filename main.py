import json
from datetime import datetime
from transform import clean_regions
from extract import *


if __name__ == '__main__':
    videoData = dict()
    channelList = set()
    channels = dict()

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    youtube = get_authenticated_service()

    # Get and clean all the regions
    regions = get_regions(youtube)
    regions = clean_regions(regions)

    # Fetch all the videos from each region and their information
    # The get_videos function already performs the cleaning process
    for region in regions.keys():
        regional_channels = get_videos(region, youtube, videoData)
        channelList |= regional_channels

    # Save today's trending videos in a json file
    today = {now: videoData}
    with open('videos.json', 'w', encoding='utf-8') as file:
        json.dump(today, file, ensure_ascii=False, indent=2)

    # Convert the channel list set into a list of 50 sized batches
    # This is done because the channel list supports a maximum of 50 results per query
    channelList = [ list(channelList)[i:i + 50] for i in range(0, len(channelList), 50) ]

    # Update the channels dictionary with the cleaned information of every batch
    for batch in channelList:
        channelIDs = ','.join(batch)
        channels.update(get_channels(channelIDs, youtube))

    # Save all the channels' information in a json file
    today = {now: channels}
    with open('channels.json', 'w', encoding='utf-8') as file:
        json.dump(today, file, ensure_ascii=False, indent=2)
