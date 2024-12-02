
# OLD SCRIPT (uses SSH and TERMUX)
- This script is for phone to run
- Your Phone needs to be rooted for this\n 
- If it is then change the permssion of folder /data/data/it.vfsfitvnm.vimusic/databases/ to 0777\n
- and also do the same in waydroid  pc folder which is in ~/.local/share/waydroid/data/data/it.vfsfitvnm.vimusic/databases/ to 0777

- Install Termux on andorid and grant super user rights to it 
- install python to termux
- you can run this script in a loop or simple run it whenver you open termux by putting it in .bashrc
- Pc and Android needs to be on same wifi

[Tasks]
- Will use Firebase to Sync the data between android and pc  X(instead using youtube api)
- instead of termux modify original app to run the script    X(will have to modify apk file to run the script independently)



# NEW SCRIPT(youtube api)
[2 JUNE Update]
Instead of updating over ssh, i am using youtube api to sync music

## Assumptions
- Termux, with python and below mentioned Dependencies
- ROOTED PHONE

## Support - vimusic, rimusic, innertune

## How to Use this?
- Go to cloud console 
- Create youtube api secrete keys and rename to client_secret.json
https://youtu.be/QY8dhl1EQfI?si=MdlroaY6Jb0x-5Uy
- Watch above video if you don't know how to create api secret..
- update PLAYLIST_ID in code with your youtube playlist id
- Run the script as root user in termux
- run vi_ytub to sync vimusic and innertune_ytub to sync innertune music
- Currently for easy of access you can this script as termux shortcut in termux widget
## [Python Dependencies]
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client


## TASKS
- Trying to merge it with original apks

