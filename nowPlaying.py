import tweepy
import requests
import time
import datetime
import os
from dotenv import load_dotenv
load_dotenv()


def getTimestamp():
    return str(datetime.datetime.now().strftime("%d %b %Y %H:%M:%S"))


def isDateNDaysInPast(fileName, n):
    date = datetime.datetime.strptime(fileName[4:-4], "%d.%b %Y")
    timeDifference = (datetime.datetime.now() - date).days
    return timeDifference > n


def clearOldLogs(currLog):
    files = os.listdir()
    logs = [name for name in files if name.startswith(
        "log") and name.endswith(".txt") and isDateNDaysInPast(name, 30)]
    for fileToDelete in logs:
        try:
            os.remove(fileToDelete)
            msg = 'Deleting log - ' + fileToDelete
            print(msg)
            currLog.write(msg + '\n')
        except:
            msg = 'Failed to delete log - ' + fileToDelete
            print(msg)
            currLog.write(msg + '\n')


emoji = '🎵'

API_KEY = os.getenv('URY_API_KEY')
URY_API_ENDPOINT = 'https://ury.org.uk/api/graphql?query=%7BnowPlaying%7Btrack%7B...%20on%20Track%7Btitle,artist%7D,...%20on%20TrackNotRec%7Btitle,artist%7D%7D%7D%7D&api_key=' + API_KEY

print(URY_API_ENDPOINT)

# Authenticate to Twitter

auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'),
                           os.getenv('CONSUMER_SECRET'))

auth.set_access_token(os.getenv('TOKEN'),
                      os.getenv('TOKEN_SECRET'))

lastPlayed = ''

# Create API object
api = tweepy.API(auth)
print('Running...')

while True:
    # get current track
    try:
        log = open(
            "log " + str(datetime.datetime.now().strftime("%d.%b %Y")) + ".txt", "a")
        clearOldLogs(log)
        r = requests.get(URY_API_ENDPOINT)
        res = r.json()
        if not res['data']['nowPlaying']:
            raise
        title = res['data']['nowPlaying']['track']['title']
        artist = res['data']['nowPlaying']['track']['artist']
        if lastPlayed != title + ' - ' + artist:
            lastPlayed = title + ' - ' + artist
            try:
                postFix = ''
                # if 'King Gizzard' in lastPlayed:
                #     postFix = ' - Did someone say vonc @alextowells - @ury1350 ?'
                api.update_status(emoji*2 + ' NOW PLAYING: ' +
                                  lastPlayed + postFix + ' ' + emoji*2)
                msg = getTimestamp() + ' tweeting: ' + lastPlayed + postFix
                print(msg)
                log.write(msg + '\n')
            except BaseException as e:
                msg = getTimestamp() + ' Failed to tweet: ' + str(e) + \
                    ' ' + lastPlayed + ' ' + postFix
                print(msg)
                log.write(msg + '\n')
    except:
        msg = 'failed to get URY data'
        print(msg)
    finally:
        log.close()
        time.sleep(10)
