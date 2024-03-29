# Imports
from __future__ import unicode_literals
import youtube_dl
from plyer import notification
import sys, getopt,os
# from playsound import playsound

class Logger(object):
    # Ignore debugs and warnings, but print errors.
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def default_hook(d):
    if d["status"] == "finished":
        # APP_ICON_LOCATION = "./RESOURCES/APP_ICON.ico"
        # # AUDIO_LOCATION = "./RESOURCES/NOTIF_AUDIO.mp3"
        # # playsound(AUDIO_LOCATION)
        # notification.notify(
        #     app_name='YTDownloader',
        #     title="Download Complete!",
        #     message="Check your output folder.",
        #     app_icon = APP_ICON_LOCATION,
        #     timeout = 5
        # )
        print("Status is Finished")

def playlist_check(result):
    if len(result) > 1:
        return True
    return False

def download(url : str, SAVE_PATH : str, type : str, quality : str, hook=None, download_all : bool = False):
    print("Beginning download for: " + url)

    hook = hook or default_hook

    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': Logger(),
    'progress_hooks': [hook],
    }


    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url,download=False)

    is_playlist = playlist_check(result=result)
    is_playlist = False
    video = result[0] if is_playlist and download_all == False else result

    if (quality != 'best') and (quality != "worst"):
        raise Exception(f"Incorrect quality type | Best or Worst only, but was given {quality}")
    
    if type == "audio":
        ydl_opts = {
        'format': f'{quality}audio/{quality}',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # 'logger': Logger(),
        'progress_hooks': [hook],
        'outtmpl': SAVE_PATH + '/%(title)s.%(ext)s'
        }
    elif type == "video":
        ydl_opts = {
            'format': f'{quality}video[ext=mp4]+{quality}audio[ext=mp4]/mp4+{quality}[height<=480]',
            # "logger": Logger(),
            'progress_hooks': [hook],
            "outtmpl": SAVE_PATH + '/%(title)s.%(ext)s'
            }
    else:
        raise Exception(f"Incorrect file type | Audio or Video only, but was given {type}")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print(is_playlist)
        if is_playlist == True:
            count = 0
            for i in video:
                count = count + 1
                print("Downloading video " + str(count))
                print(i)
                i = "https://youtu.be/" + i.get("id")
                print(i)
                os.system("python downloader.py -u " + i + " -p " + SAVE_PATH + " -t " + type + " -q " + quality + " -a " + download_all)
        else:
            ydl.download([url])

def get_data(url: str):
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': Logger(),
    'progress_hooks': [default_hook]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url,download=False)

    # Checks if this is a playlist
    if len(result > 1):
        print("Playlist provided!")
        print("Grabbing first video.")

        video = result['entries'][0]
    else:
        video = result

    return video

def main(argv):
    url = ""
    path = "./downloads"
    type = "video"
    quality = "worst"
    all = False

    try:
        opts, args = getopt.getopt(argv,"hu:p:t:q:a:") 
    except getopt.GetoptError:
        print ('downloader.py -u <url> -p <path> -t <type> -q <quality> -a <all>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('downloader.py -u <url> -p <path> -t <type> -q <quality> -a <all>')
            sys.exit()
        elif opt in ("-u"):
            url = arg
        elif opt in ("-p"):
            path = arg
        elif opt in ("-t"):
            type = arg
        elif opt in ("-q"):
            quality = arg
        elif opt in ("-a"):
            all = arg

    print(url)

    download(url,path,type,quality,all)

if __name__ == "__main__":
   if len(sys.argv) > 1: 
        main(sys.argv[1:])