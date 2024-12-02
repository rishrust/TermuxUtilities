import sqlite3
import os
# import sync
from sync import *
from time import sleep




# database_path = "/home/rish/data/PROJECTS/innertune/NEW_INNERTUNE/com.zionhuang.music/databases/song.db"
database_path = "/home/rish/.local/share/waydroid/data/data/com.zionhuang.music/databases/song.db"
yt = get_authenticated_service()
# Authenticate and create a YouTube service
youtube = yt

def get_private_playlists(youtube):
    playlists = []
    
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        mine=True,
        maxResults=50  # Max number of playlists to retrieve in one request
    )
    
    while request:
        response = request.execute()
        playlists.extend(response.get('items', []))
        
        # Check if there's another page of results
        request = youtube.playlists().list_next(request, response)
    
    # return playlists
    playlist_info=[]
    for playlist in playlists:
        # print(f"Playlist Title: {playlist['snippet']['title']}")
        p={}
        p['title']  = playlist['snippet']['title']
        p['id']  = playlist['id']
        p['Description'] = playlist['snippet']['description']
        playlist_info.append(p)
        # print(f"Playlist ID: {playlist['id']}")
        # print(f"Description: {playlist['snippet']['description']}")
        # print(f"Number of Videos: {playlist['contentDetails']['itemCount']}")
        # print("-" * 50)
    return playlist_info




# print(playlist_info)



#from youtube to innertune

# checks whether youtube playlist are present in app
def check_in_app(playlist_info):
    missing = []
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    for playlist in playlist_info:
        cursor.execute("SELECT COUNT(*) FROM playlist WHERE id = ?;", (playlist['id'],))
        count = cursor.fetchone()[0]
        if(count == 0 ):
            missing.append(playlist['id'])
        return missing
    connection.close()





# add from youtube to app
def youtube_to_innertunev2(playlist_info):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    print(playlist_info)
    for playlist in playlist_info:
        # checking whether playlist exists
        cursor.execute("SELECT COUNT(*) FROM playlist WHERE id = ?;", (playlist['id'],))
        playlist_status  = cursor.fetchone()[0]
        if(playlist_status == 0 ):
            cursor.execute("INSERT INTO playlist (id, name) VALUES (?, ?);",(playlist['id'],playlist['title'],))
        
        # checking whether songs exist in app 
        playlist_songs = get_songs_from_youtube_playlist(playlist['id'])
        # print(playlist_songs)
        for song in playlist_songs:
            song_id = song['snippet']['resourceId']['videoId']
            cursor.execute("SELECT COUNT(*) FROM playlist_song_map WHERE songid = ?;", (song_id,))
            song_status =  cursor.fetchone()[0]
            if(song_status == 0 ): 
                cursor.execute("SELECT MAX(position) AS max_position FROM playlist_song_map WHERE playlistid = ?;",(playlist["id"],))
                position = cursor.fetchone()
                if(position[0] == None):
                    position=0
                else:
                    position=position[0]+1
                    print("adding songs")

                cursor.execute("INSERT INTO playlist_song_map (playlistid, songid, position) VALUES(?,?,?);",(playlist["id"], song_id,position) )
                youtube_to_innertune_commit(playlist['id'],database_path,cursor)
    connection.commit()
    connection.close()







# get playlist from innertune
def get_innertune_playlists():
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("SELECT id from playlist")
    playlists = cursor.fetchall() 
    tmp = []
    for i in playlists:
        cursor.execute("select name from playlist where id = ?",(i[0],))
        tmp.append(i[0])
    connection.close()
    return tmp


youtube_to_innertunev2(get_private_playlists(youtube))
print(get_innertune_playlists())




def get_innertune_songs(playlist_id):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("SELECT songid from playlist_song_map where playlistid = ?;",(playlist_id,))
    playlist_songs = cursor.fetchall()
    songs = []
    for i in playlist_songs:
        songs.append(i[0])

    connection.close()
    return songs



def create_playlist_youtube(youtube, title, description):
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['sample playlist', 'API'],
            'defaultLanguage': 'en'
        },
        'status': {
            'privacyStatus': 'private'  # 'public' or 'unlisted'
        }
    }

    try:
        response = youtube.playlists().insert(
            part='snippet,status',
            body=request_body
        ).execute()

        print(f"Playlist created with ID: {response['id']}")
        return response['id']
    except HttpError as e:
        print(f"An error occurred: {e}")
        return None

# add from app to youtube
def innertune_to_youtube():
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    innertune_playlists = get_innertune_playlists()
    youtube_playlists = get_private_playlists(youtube)

    for playlist in innertune_playlists:
        playlist_status = 0
        if playlist[0] in youtube_playlists:
            playlist_status = 1
        if playlist_status == 0:  # now time to add in youtube and modify key in app
            playlist_id = create_playlist_youtube(youtube, playlist[1],"created from innertune")
            # now change playlist id
            cursor.execute("UPDATE playlist_song_map SET playlistid = ? WHERE playlistid = ?;",(playlist[0],playlist_id,))
            cursor.execute("UPDATE playlist SET id = ? WHERE id = ?;",(playlist[0],playlist_id,))

            songs = get_innertune_songs(playlist_id)
            

        else:
            pass  
            
        connection.close()