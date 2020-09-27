import tweepy
import requests
import time
import datetime

def getTimestamp():
    return str(datetime.datetime.now().strftime("%d %b %Y %H:%M:%S"))

emoji = '🎵'

API_KEY = ''
URY_API_ENDPOINT = 'https://ury.org.uk/api/graphql?query=%7BnowPlaying(include_playout:false)%7Btrack%7B...%20on%20Track%7Btitle,artist%7D,...%20on%20TrackNotRec%7Btitle,artist%7D%7D%7D%7D&api_key=' + API_KEY

# Authenticate to Twitter

auth = tweepy.OAuthHandler("", "")
auth.set_access_token("", "")
lastPlayed = ''

# Create API object
api = tweepy.API(auth)
print('Running...')

while True:
    # get current track
    try:
        log = open("log " + str(datetime.datetime.now().strftime("%d.%b %Y")) + ".txt","a")
        r = requests.get(URY_API_ENDPOINT)
        res = r.json()
        if not res['data']['nowPlaying']:
            raise;
        title = res['data']['nowPlaying']['track']['title']
        artist = res['data']['nowPlaying']['track']['artist']
        if lastPlayed != title + ' - ' + artist:
            lastPlayed = title + ' - ' + artist
            try:
                postFix = ''
                # if 'King Gizzard' in lastPlayed:
                #     postFix = ' - Did someone say vonc @alextowells - @ury1350 ?'
                api.update_status(emoji*2 + ' NOW PLAYING: ' + lastPlayed  +  postFix + ' ' + emoji*2)
                msg = getTimestamp() + ' tweeting: ' + lastPlayed + postFix
                print(msg)
                log.write(msg + '\n')
            except BaseException as e:
                msg = getTimestamp() + ' Failed to tweet: ' + str(e) + ' ' + lastPlayed + ' ' + postFix
                print(msg)
                log.write(msg + '\n')
    except:
        msg = 'failed to get URY data'
        print(msg)
    finally:
        log.close()
        time.sleep(10)
