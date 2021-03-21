import requests
import json
import datetime
import csv
from YoutubeAPI import YoutubeAPI


f = open("apikey.txt")

API_KEY = f.read()
api = YoutubeAPI(API_KEY)

id_channel = "UCNRYbltJXhf6DepS26-uSbQ"

playlists = api.get_playlist(id_channel)

videos = api.get_videos_by_list_playlists(playlists)

keys = videos[0].keys()

with open('outputfile.csv', 'w', newline='', encoding='utf-8')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys, delimiter=';')
    dict_writer.writeheader()
    dict_writer.writerows(videos)

