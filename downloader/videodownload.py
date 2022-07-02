import tweepy
from tweepy import parsers
import re
from dotenv import load_dotenv
import os
import json
from datetime import timedelta
import numpy as np

load_dotenv()

bearer_token = os.getenv("BEARER_TOKEN")
consumer_key = os.getenv("API_KEY")
consumer_secret = os.getenv('API_KEY_SECRET')
access_token = os.getenv('Access_Token')
access_token_secret = os.getenv('Access_Token_Secret')

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


def request_video(url_link):
    links = []
    tweet_link = url_link

    tweet_id = tweet_link.split("/")[-1].split('?')[0]

    status = api.get_status(tweet_id, tweet_mode="extended")

    thumb = status["extended_entities"]["media"][0]["media_url"]

    created_at = str(status["created_at"]).replace('-', '+').split('+')[0]

    try:
        duration = str(timedelta(milliseconds=status["extended_entities"]["media"][0]["video_info"]
                            ["duration_millis"])).split(".")[0]

        raw_duration = str(status["extended_entities"]["media"][0]["video_info"]["duration_millis"])
    except:
        duration = "None"
        raw_duration = "None"

    if str(status["user"]["name"]):
        user = status["user"]["name"]
    else:
        user= ""


    # print(json.dumps(status, sort_keys=True, indent=4))

    i = 0

    qualities = []
    bitrate= []
    type=""

    while True:
        try:

            if status["extended_entities"]["media"][0]["type"] == "video":

                video_info = status["extended_entities"]["media"][0]["video_info"]["variants"][i]["url"]

                if ".mp4?tag" in video_info:
                    bitrate.append(status["extended_entities"]["media"][0]["video_info"]["variants"][i]["bitrate"])
                    links.append(video_info)
                    aspect_ratio = re.findall("[0-9]+x[0-9]+", video_info)[0]
                    qualities.append(aspect_ratio)
                    type="Video"

                else:
                    i = i + 1
                    continue
                i = i + 1
            else:
                video_info = status["extended_entities"]["media"][0]["video_info"]["variants"][0]["url"]
                links.append(video_info)
                qualities.append("None")
                type="GIF"

                break
        except:
            break

    return links, qualities, thumb, created_at, duration, user, type

