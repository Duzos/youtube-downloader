import asyncio
from tkinter import *
import downloader

class App:
    async def exec(self):
        self.window = Window(asyncio.get_event_loop)
        await self.window.show()

class Window(Tk):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop
        self.root = Tk()
        # URL SIDE
        url_frame = Frame(master=self.root, relief=GROOVE,borderwidth=5)
        url_frame.pack(side=LEFT)

        self.url_label = Label(text="YouTube URL:", master=url_frame)
        self.url_box = Entry(master=url_frame)
        url_button = Button(text="Download",command=lambda: asyncio.create_task(self.url_button_click()),master=url_frame)
        url_status_label = Label(master=url_frame)

        self.url_label.pack()
        self.url_box.pack()
        url_button.pack()
        url_status_label.pack()

    async def show(self):
        while True:
            self.root.update()
            await asyncio.sleep(.1)


    async def url_button_click(self):
        url = self.url_box.get()
        
        await downloader.progress(url)

asyncio.run(App().exec())