import sqlite3
import os
import sync
from sync import to_youtube,get_songs_from_youtube_playlist,get_youtube_playlist_songs
from time import sleep
PLAYLIST_ID="PLga65AAwFBxh8oWz0P0cq8XafewLx6Qga"

#changing permission of vimusic folder
print("changing permission of vimusic folder")
os.system("sudo chmod 0777 -R /data/data/it.vfsfitvnm.vimusic/databases/")



class vi_db:
    title=""
    video_id=""
    artistsText=""
    durationText="-"
    thumbnailUrl=""
    likedAt="-"
    totalPlayTimeMs="-"

# SYNC vimusic >> youtube;;

db_file = '/data/data/it.vfsfitvnm.vimusic/databases/data.db'
# db_file='/home/rish/data/PROJECTS/innertune/vimsuic_db/data.db'

# get liked music from vi music
def get_liked_music(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    query = "SELECT * FROM song"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    print("Attributes:", columns)
    rows = cursor.fetchall()

    liked=[]
    for row in rows:
        current_id=0
        for column, value in zip(columns, row):
            if column=="id":
                current_id=value
            
            if column=="likedAt":
                if value!=None:
                    liked.append(current_id)
                break
            
    for i in liked:
        print(i)
    
    cursor.close()
    conn.close()
    return liked





#sync liked music with youtube
def vi_liked_to_youtube(local_liked):
    ytube_liked=get_youtube_playlist_songs(PLAYLIST_ID)
    for i in local_liked:
        if i not in ytube_liked:
            to_youtube(i,PLAYLIST_ID)
            sleep(0.1)



# Sync music from youtube to vimusic

def youtube_to_vi_help(db_file, title, video_id, thumbnailUrl, artistsText):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Check if the video_id already exists in the database
    cursor.execute('SELECT COUNT(*) FROM song WHERE id = ?', (video_id,))
    result = cursor.fetchone()

    if result[0] == 0:
        # If video_id does not exist, insert the new record
        cursor.execute('''
        INSERT INTO song 
        (id, title, thumbnailUrl, artistsText,totalPlayTimeMs,likedAt)
        VALUES (?, ?, ?, ?, ?, ? )
        ''', (video_id, title, thumbnailUrl, artistsText, '-',1921212121))
        
        conn.commit()
        print("Record inserted successfully.")
    else:
        print("Record already exists.")
    
    conn.close()



def youtube_to_vi(PLAYLIST_ID):
    all_songs=get_songs_from_youtube_playlist(PLAYLIST_ID)

    for song in all_songs:
        title=song['snippet']['title']
        video_id=song['snippet']['resourceId']['videoId']
        thumbnailUrl=song['snippet']['thumbnails']['default']['url']
        artistsText=song['snippet']['videoOwnerChannelTitle']
        if " - Topic" in artistsText:
            artistsText=artistsText.strip(" - Topic")
        
        youtube_to_vi_help(db_file,title,video_id,thumbnailUrl,artistsText)


    






vi_liked_to_youtube(get_liked_music(db_file))
youtube_to_vi(PLAYLIST_ID)




# Iterate over the rows and print each row along with its corresponding attribute names
# for row in rows:
#     for column, value in zip(columns, row):
#         print(f"{column}: {value}")
#     print()  # Print a newline between rows

# Close the cursor and the connection
