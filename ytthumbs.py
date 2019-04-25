# CS35 Project
# ytthumbs.py


import os
import time
import json
import urllib.request
import googleapiclient.discovery


API_KEY = 'YOUR_API_KEY_HERE'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
api_service_name = 'youtube'
api_version = 'v3'


youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = API_KEY)




def getChannelID(username):
    """ Returns string channel identifier for string
        of legacy YT username.
    """
    request = youtube.channels().list(
        part = 'id', forUsername = username)
    response = request.execute()

    channelID = response['items'][0]['id']
    return channelID



def getUploadsID(channel, username=False):
    """ Returns string of a channel's Uploads playlist 
        id. Input default is channel id, can do username.
    """
    if username:
        request = youtube.channels().list(
        part = 'contentDetails', forUsername = channel)
    else:
        request = youtube.channels().list(
        part = 'contentDetails', id = channel)
    response = request.execute()

    uploadsID = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return uploadsID




def getVideoList(playlistID, maxVids=5000, perPage=50, filename=''):
    """
    """
    videos = []
    
    request = youtube.playlistItems().list(
    part='contentDetails', maxResults = perPage, playlistId = playlistID)
    
    while request is not None and len(videos) < maxVids:
        
        response = request.execute()

        for item in response['items']:
            vid = item['contentDetails']['videoId']
            videos.append(vid)

        request = youtube.playlistItems().list_next( request, response )     

    if not filename == '':
        filetext = ''
        for vid in videos:
            filetext += vid + ',\n'
        print(filetext,  file=open( filename + '.csv', 'w'))

    return videos



def saveThumb(videoID, size='mqdefault', filename=''):
    """ Saves a local copy of a video's thumbnail.
        videoID: YT video identification string (after ?v=)
        size: String of thumbnail variant
            0, 1, 2, 3, default, mqdefault, hqdefault
        filename: .jpg string, defaults to videoID
    """
    if filename == '':
        filename = videoID + '.jpg'

    try:
        url = 'https://img.youtube.com/vi/' + videoID + '/' + size + '.jpg'
        urllib.request.urlretrieve( url, filename )
        print('Saved thumbnail of video', videoID)
    except:
        print('ERROR on video', videoID)



def saveBatch(IDlist, delay=1):
    """
    """
    for ID in IDlist:
        saveThumb(ID)
        time.sleep(delay)
