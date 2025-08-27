from googleapiclient.discovery import build
import os


class YoutubeAPI:

    def __init__(self):
        self.api_key = os.environ["YOUTUBE_API_KEY"]
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.query = ""
    
    def getChannelThumbnail(self,channel_id):
        request = self.youtube.channels().list(
        part='snippet',
        id=channel_id
        )
        response = request.execute()
        if response.get('items'):
            thumbnail_url = response['items'][0]['snippet']['thumbnails']['default']['url']
            return thumbnail_url

    def statistics(self, id):
        statistics_request = self.youtube.videos().list(
            part="statistics",
            id = id
        )
        statistics_response = statistics_request.execute()
        return statistics_response
    def search(self):
        request = self.youtube.search().list(
            q = self.query,
            part = 'snippet',
            maxResults = 100,
            type='video',
            # videoCategoryId = '28'
        )
        response = request.execute()
        result = {}
        vidNo = 1
        for i in response.get('items'):
           
            content = {}
            # if (i['id']['kind'] == "youtube#video"):
            title = i['snippet']['title'].lower()
            description = i['snippet']['description'].lower()
           
            if (not ('nude' in title or 'nude' in description or 'sex' in title or 'sex' in description or 'orgasm' in title or 'orgasm' in description or 'intercourse' in title or 'intercourse' in description) and ('course' in title or 'course' in description or 'tutorial' in title or 'tutorial' in description or 'lesson' in title or 'lesson' in description or 'learn' in title or 'learn' in description or 'education' in title or 'education' in description or 'note' in title or 'note' in description)):
            
                content['id'] = i['id']
                content['snippet'] = i['snippet']
                content['items'] = self.statistics(i['id']['videoId'])['items']
                content['channel_thumbnail'] = self.getChannelThumbnail(i['snippet']['channelId'])
              
                result[vidNo] = content
                vidNo += 1
        return result
    
    def getVideoDetails(self, videoId):
        request = self.youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=videoId
        )
        response = request.execute()
    
        video_details = response['items'][0]
    
        snippet = video_details['snippet']
        title = snippet['title']
        description = snippet['description']
        thumbnail_url = snippet['thumbnails']['default']['url']
        published_at = snippet['publishedAt']  # New line to get published time
    
        content_details = video_details['contentDetails']
        duration = content_details['duration']
    
        statistics = video_details['statistics']
        view_count = statistics['viewCount']
        like_count = statistics.get('likeCount', 0)
        dislike_count = statistics.get('dislikeCount', 0)
        comment_count = statistics.get('commentCount', 0)
    
        channel_id = snippet['channelId']
        request = self.youtube.channels().list(
            part='snippet',
            id=channel_id
        )
        channel_response = request.execute()
        channel_snippet = channel_response['items'][0]['snippet']
        channel_title = channel_snippet['title']
        channel_thumbnail_url = channel_snippet['thumbnails']['default']['url']
    
        video_info = {
            'title': title,
            'description': description,
            'thumbnail_url': thumbnail_url,
            'duration': duration,
            'view_count': view_count,
            'like_count': like_count,
            'dislike_count': dislike_count,
            'comment_count': comment_count,
            'channel_title': channel_title,
            'channel_thumbnail_url': channel_thumbnail_url,
            'published_at': published_at  # Add published time to the dictionary
        }
    
        return video_info
    
    
