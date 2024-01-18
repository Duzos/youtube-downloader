from downloader import *
from tkinter import *

window = Tk()
window.title = "YouTube Downloader"

def display_hook(d):
    if d['status'] == 'finished':
        url_status_label["text"] = 'Finished downloading'
    if d['status'] == 'downloading':
        url_status_label["text"] = "{} : {} {}".format(d["filename"],d["_percent_str"],d["_eta_str"])

def url_button_click():
    url = url_box.get()
    path = settings_save_path_entry.get()
    type = settings_type_button["text"]
    quality = settings_quality_button["text"]
    all = True if settings_playlist_button["text"] == "true" else False
    
    download(url=url,SAVE_PATH=path,type=type,quality=quality, download_all=all,hook=display_hook)

def type_button_click():
    if settings_type_button["text"] == "video":
        settings_type_button["text"] = "audio"
    elif settings_type_button["text"] == "audio":
        settings_type_button["text"] = "video"
    else:
        raise Exception("Type button toggle failed.")

def quality_button_click():
    if settings_quality_button["text"] == "worst":
        settings_quality_button["text"] = "best"
    elif settings_quality_button["text"] == "best":
        settings_quality_button["text"] = "worst"
    else:
        raise Exception("Quality button toggle failed.")

def playlist_button_click():
    if settings_playlist_button["text"] == "true":
        settings_playlist_button["text"] = "false"
    elif settings_playlist_button["text"] == "false":
        settings_playlist_button["text"] = "true"
    else:
        raise Exception("Quality button toggle failed.")

# SETTINGS SIDE
settings_frame = Frame(master=window,borderwidth=5)
settings_frame.pack(side=RIGHT)

settings_header_label = Label(text="SETTINGS:",master=settings_frame)

settings_save_path_label = Label(text="Save Path:",master=settings_frame)
settings_save_path_entry = Entry(text="./downloads",master=settings_frame)

settings_type_label = Label(text="Type:",master=settings_frame)
settings_type_button = Button(text="video", command=type_button_click,master=settings_frame)

settings_quality_label = Label(text="Quality:", master=settings_frame)
settings_quality_button = Button(text="best", command=quality_button_click,master=settings_frame)

settings_playlist_label = Label(text="PLAYLIST SETTINGS:\n\nDownload All Videos:", master=settings_frame)
settings_playlist_button = Button(text="false", command=playlist_button_click,master=settings_frame)

settings_header_label.pack()
settings_save_path_label.pack()
settings_save_path_entry.pack()
settings_type_label.pack()
settings_type_button.pack()
settings_quality_label.pack()
settings_quality_button.pack()
settings_playlist_label.pack()
settings_playlist_button.pack()

# URL SIDE
url_frame = Frame(master=window, relief=GROOVE,borderwidth=5)
url_frame.pack(side=LEFT)

url_label = Label(text="YouTube URL:", master=url_frame)
url_box = Entry(master=url_frame)
url_button = Button(text="Download",command=url_button_click,master=url_frame)

url_status_label = Label(master=url_frame)

url_label.pack()
url_box.pack()
url_button.pack()
url_status_label.pack()

window.mainloop()
