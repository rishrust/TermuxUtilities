import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request

# Set up the necessary scopes and API service name
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"  # Replace with your client secret JSON file
token_pickle_file = "token.pickle"  # File to store the token

def get_authenticated_service():
    credentials = None
    # Load credentials from the token file if it exists
    if os.path.exists(token_pickle_file):
        with open(token_pickle_file, 'rb') as token:
            credentials = pickle.load(token)
    
    # If there are no valid credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
            credentials = flow.run_local_server(port=9213)
        # Save the credentials for the next run
        with open(token_pickle_file, 'wb') as token:
            pickle.dump(credentials, token)
    
    return googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

def check_if_video_in_playlist(youtube, playlist_id, video_id):
    # Fetch the playlist items
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50  # Adjust as needed
    )
    response = request.execute()
    
    # Check if the video ID is in the playlist
    for item in response['items']:
        if item['snippet']['resourceId']['videoId'] == video_id:
            return True
    return False



def get_youtube_playlist_songs( playlist_id):
    youtube = get_authenticated_service()
     # Fetch the playlist items
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50  # Adjust as needed
    )
    response = request.execute()
    songs=[]
    # Check if the video ID is in the playlist
    for item in response['items']:
        songs.append(item['snippet']['resourceId']['videoId'])

    return songs




def add_song_to_playlist(youtube, playlist_id, video_id):
    if check_if_video_in_playlist(youtube, playlist_id, video_id):
        print(f"Video {video_id} is already in the playlist.")
        return None

    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    return response



    


        # Replace with your playlist ID and video ID

def to_youtube(video_id,playlist_id):
    # playlist_id = "PLga65AAwFBxh8oWz0P0cq8XafewLx6Qga"
    # playlist_id = "3_g2un5M350"
    youtube = get_authenticated_service()
    response = add_song_to_playlist(youtube, playlist_id, video_id)
    if response:
        print(f"Added video to playlist: {response['snippet']['title']}")













def get_playlist_items_utils(service, **kwargs):
    results = service.playlistItems().list(**kwargs).execute()
    return results['items']

def get_songs_from_youtube_playlist(playlist_id):
    # Disable OAuthlib's HTTPS verification when running locally.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Get the authenticated service
    service = get_authenticated_service()

    # The ID of the playlist from which to retrieve items
    # playlist_id = "YOUR_PLAYLIST_ID"

    # Fetch the first page of playlist items
    playlist_items = get_playlist_items_utils(service, part="snippet", maxResults=50, playlistId=playlist_id)

    all_songs = []
    all_songs.extend(playlist_items)

    # Continue fetching playlist items if there are more pages
    while 'nextPageToken' in playlist_items:
        playlist_items = get_playlist_items(service, part="snippet", maxResults=100, playlistId=playlist_id, pageToken=playlist_items['nextPageToken'])
        all_songs.extend(playlist_items)

    # Print out the titles of the songs
    for item in all_songs:
        title = item['snippet']['title']
        video_id = item['snippet']['resourceId']['videoId']
        print(item['snippet'])
        # print(item)
        # print(video_id)
    

    return all_songs
