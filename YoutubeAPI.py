import requests
import json
import datetime

def get_seconds_by_str(s: str):
    try:
        a = datetime.datetime.strptime(s, "PT%HH%MM%SS").time()
        return a.hour * 60 * 60 + a.minute * 60 + a.second
    except Exception:
        try:
            a = datetime.datetime.strptime(s, "PT%MM%SS").time()
            return a.hour * 60 * 60 + a.minute * 60 + a.second
        except Exception:
            return -1


class YoutubeAPI:
    def __init__(self, key):
        self.key_api = key

    def get_playlist(self, id_channel):
        next_page_token = ""
        is_first = True
        playlists = []

        while True:
            url = "https://www.googleapis.com/youtube/v3/playlists?channelId={0}&key={1}" \
                  "&maxResults=50&part=snippet,contentDetails".format(id_channel, self.key_api)
            if not is_first:
                url = url + "&pageToken=" + next_page_token
            response = requests.get(url)

            if response.status_code != 200:
                print(response.content)
                exit(0)

            data = json.loads(response.text)

            for item in data["items"]:
                playlists.append(item)

            if "nextPageToken" in data.keys():
                next_page_token = data["nextPageToken"]
            else:
                next_page_token = None
            if next_page_token is None or next_page_token == "":
                break
            is_first = False

        return playlists

    def add_videos_by_ids(self, ids, videos, playlist):
        if len(ids) > 50:
            cnt = 0
            while cnt < len(ids):
                self.add_videos_by_ids(ids[cnt:(cnt+45)], videos, playlist)
                cnt += 45
        else:
            url = "https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&key={0}" \
                   "&id={1}".format(self.key_api, ','.join(map(str, ids)))
            response = requests.get(url)

            if response.status_code != 200:
                print(url)
                print(response.content)
                exit(0)

            data = json.loads(response.text)

            for video in data["items"]:
                videos.append({
                    "name_playlist": playlist["snippet"]["title"],
                    "name_video": video["snippet"]["title"],
                    "published": video["snippet"]["publishedAt"],
                    "view_count": video["statistics"]["viewCount"],
                    "like_count": video["statistics"]["likeCount"],
                    "dislike_count": video["statistics"]["dislikeCount"],
                    "favorite_count": video["statistics"]["favoriteCount"],
                    "comment_count": video["statistics"]["commentCount"],
                    "duration": get_seconds_by_str(video["contentDetails"]["duration"])
                })

    def get_videos_by_list_playlists(self, playlists):
        videos = []
        for playlist in playlists:
            is_first = True
            next_page_token = ""
            ids_videos = []
            while True:
                link = "https://www.googleapis.com/youtube/v3/playlistItems?playlistId={0}&key={1}" \
                       "&part=snippet,contentDetails".format(playlist["id"], self.key_api)
                if not is_first:
                    link = link + "&pageToken=" + next_page_token
                response = requests.get(link)
                if response.status_code != 200:
                    print(link)
                    print(response.content)
                    exit(0)
                data = json.loads(response.text)

                for item in data["items"]:
                    ids_videos.append(item["snippet"]["resourceId"]["videoId"])

                self.add_videos_by_ids(ids_videos, videos, playlist)

                if "nextPageToken" in data.keys():
                    next_page_token = data["nextPageToken"]
                else:
                    next_page_token = None
                if next_page_token is None or next_page_token == "":
                    break
                is_first = False

            # break
        return videos






