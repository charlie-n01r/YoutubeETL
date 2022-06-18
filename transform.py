def get_items(data):
    # Get only the snippet of the request's response
    data = data['items']
    cleaned = dict()

    return data, cleaned


def clean_regions(data):
    data, cleaned = get_items(data)

    # Create an entry in the dictionary using the region code as key and the name as its value
    for region in data:
        snippet = region['snippet']
        cleaned[snippet['gl']] = snippet['name']

    return cleaned


def clean_video_list(data):
    data, video_list = get_items(data)
    channels = list()

    for item in data:
        # For every video in the video list, create a new entry using the videoID as key
        key = item['id']
        snippet = item['snippet']

        # Get the important information from the video's data
        title = snippet['title']
        published_date = snippet['publishedAt']
        channel = snippet['channelId']
        statistics = item['statistics']
        # Not all videos have tags or the audio language, so it's important to set the value of those who don't as null
        language = snippet['defaultAudioLanguage'] if 'defaultAudioLanguage' in snippet.keys() else None
        tags = snippet['tags'] if 'tags' in snippet.keys() else None

        video_list[key] = {
            'title': title,
            'published_date': published_date,
            'channel': channel,
            'language': language,
            'tags': tags,
            'statistics': statistics
        }
        channels.append(channel)

    return video_list, set(channels)


def clean_channels(data):
    print(data)