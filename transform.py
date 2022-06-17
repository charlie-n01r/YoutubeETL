def clean_regions(data):
    data = data['items']
    cleaned = {}

    for region in data:
        snippet = region['snippet']
        cleaned[snippet['gl']] = snippet['name']

    return cleaned
