# -*- coding:utf-8 -*-
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import sys
import os
import json
import urllib.request
from time import sleep
import re

url_trans_smt = "https://openapi.naver.com/v1/language/translate"
url_detect_langs = "https://openapi.naver.com/v1/papago/detectLangs"

#for twitter API key
CONSUMER_KEY = '#'
CONSUMER_SECRET = '#'
ACCESS_TOKEN_KEY = '#'
ACCESS_TOKEN_SECRET = '#'

#for naver API key
client_id = "#"
client_secret = "#"


def detect_langs(encText):
    data = "query=" + encText
    request = urllib.request.Request(url_detect_langs)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    try:
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            lenC = response_body.decode('utf-8')
        else:
            print("Error Code:" + rescode)
        return json.loads(lenC)['langCode']
    except:
        print('detect_langs function is Error')
        return 'false'

def trans_smt(encText):
    data = "source=ja&target=ko&text=" + encText
    request_ = urllib.request.Request(url_trans_smt)
    request_.add_header("X-Naver-Client-Id",client_id)
    request_.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request_, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        json_dict = json.loads(response_body)
        if 'message' in json_dict:
            text = json_dict['message']['result']['translatedText']
            text = text.replace("@", "")
        return text
    elif(rescode==429):
        print("Error Code:" + rescode)


class listener(StreamListener):
    def on_data(self, raw_data):
        encText=''
        data = json.loads(raw_data)
        try:
            if 'retweeted' in data:
                try:
                    writer = data['entities']['user_mentions'][0]['screen_name']
                    encText = urllib.parse.quote(data['retweeted_status']['extended_tweet']['full_text'])
                    print(data['retweeted_status']['extended_tweet']['full_text'])
                except:
                    encText = urllib.parse.quote(data['retweeted_status']['text'])
                    print(data['retweeted_status']['text'])
                finally:
                    data=''
                    encText = result = re.sub(r"http\S+", "", encText)
                    local_dect = detect_langs(encText)
                    print(local_dect)
                    if(local_dect=="ja"):
                        try:
                            trans = trans_smt(encText)
                            trans="[from: "+writer+"]\n"+trans
                            print(trans)
                            if(len(trans) < 140):
                                api.update_status(trans)
                            else:
                                api.update_status(trans[0:140])
                                api.update_status(trans[140:])
                        except Exception as e:
                            print(e)
            elif 'delete' in data:
                data=''
            elif 'friends' in data:
                data=''
            else:
                data=''
            return True
        except:
            print('')
    def on_error(self, status):
        if status_code == 429:
            print("API limit")


if __name__ == "__main__":
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    twitterStream = Stream(auth, listener())
    twitterStream.userstream(encoding="utf-8")
