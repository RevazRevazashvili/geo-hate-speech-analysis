import re
from googleapiclient.discovery import build

api_key = "AIzaSyAIq1qYxHW3Ig1Kj-RJmGE2oJKKfnip7mg"


def is_valid(url):
    valid = True
    if url is None or not isinstance(url, str) or "youtube.com" not in url:
        valid = False
    return valid


def get_video_id(url):
    video_id = None
    try:
        video_id = re.findall(pattern=r"watch\?v=(.*)&", string=url, flags=re.IGNORECASE)[0]
    except Exception as e:
        pass

    return video_id


def transliterate_to_georgian(text):
    transliteration_dict = {
        'a': 'ა',
        'b': 'ბ',
        'g': 'გ',
        'd': 'დ',
        'e': 'ე',
        'v': 'ვ',
        'z': 'ზ',
        't': 'თ',
        'i': 'ი',
        'k': 'კ',
        'l': 'ლ',
        'm': 'მ',
        'n': 'ნ',
        'o': 'ო',
        'p': 'პ',
        'zh': 'ჟ',
        'r': 'რ',
        's': 'ს',
        'T': 'ტ',
        'u': 'უ',
        'f': 'ფ',
        'q': 'ქ',
        'gh': 'ღ',
        'y': 'ყ',
        'sh': 'შ',
        'ch': 'ჩ',
        'ts': 'ც',
        'c': 'ც',
        'dz': 'ძ',
        'ts': 'წ',
        'w': 'წ',
        'ch': 'ჭ',
        'kh': 'ხ',
        'x': 'ხ',
        'j': 'ჯ',
        'h': 'ჰ',
    }

    georgian_text = ''
    for char in text.lower():
        if char in transliteration_dict:
            georgian_text += transliteration_dict[char]
        else:
            georgian_text += char

    return georgian_text


def parse_comments(url):
    if is_valid(url):
        video_id = get_video_id(url)
        if video_id:
            pattern = re.compile(r'[a-zA-Zა-ჰ]+')
            next_page_token = None
            youtube = build('youtube', 'v3', developerKey=api_key)
            while True:
                comments_request = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    maxResults=50,  # Adjust the number of comments to retrieve per page
                    pageToken=next_page_token
                )
                try:
                    comments_response = comments_request.execute()

                    for comment in comments_response['items']:
                        comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']

                        # Use the regex pattern to extract only English and Georgian letters
                        filtered_comment = ' '.join(pattern.findall(comment_text))
                        transliterated_comment = transliterate_to_georgian(text=filtered_comment)
                        yield transliterated_comment

                    # Check if there are more pages of comments
                    if 'nextPageToken' in comments_response:
                        next_page_token = comments_response['nextPageToken']
                    else:
                        break
                except Exception as e:
                    pass
