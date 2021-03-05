import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
import requests
import json
import m3u8
import subprocess
import threading
from os import path


class AsyncDownload(Thread):
    def __init__(self , main_path):
        super().__init__()

        self.main_path = main_path
        

    def run(self):
        char = ''

        main_path_length = len(self.main_path)
        count= main_path_length -1
        url_cmp = ""
        for i in range(main_path_length):
            char = self.main_path[count]
            url_cmp+=char
            if(char=="/"):
                break
            count-=1
        fileNameInUrl = ""
        count_file_name = len(url_cmp) -1
        while(count_file_name>=0):
            fileNameInUrl+=url_cmp[count_file_name]
            count_file_name-=1
        file_path="./"
        url_info = self.main_path.replace(fileNameInUrl , " ")
        url_cmp = fileNameInUrl.lstrip("/")
        url_info = url_info.rstrip(" ")+"/"
        file_name = url_cmp.rstrip(".m3u8")
        url_1 = url_info + url_cmp
        r_1 = requests.get(url_1)
        m3u8_master = m3u8.loads(r_1.text)
        file_number = 0
        i = 0
        percentage = 0.0

        print('Download started.......')
        total  = 100
        for segment in m3u8_master.data['segments']:
            file_number += 1
        # bar = progressbar.ProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = file_number)
        # progress_bar = tqdm(total=file_number, unit_scale=True, desc=file_name, ascii=True)
        
        with open(file_path + file_name + '.ts', 'wb') as f:
            for segment in m3u8_master.data['segments']:
                url = url_info + segment['uri']
                while(True):
                    try:
                        r = requests.get(url,timeout = 15)
                    except:
                        continue
                    break

                f.write(r.content)
                i += 1
                percentage = i/file_number * 100
                # progress_bar.update(i/2)
                print("[" , end="")
                print( f"{(str(percentage))[0:5]} %",end = "")
                # print("\r\x1b[20C[",end = "")
                print("]" , end="")
                print( f"="*int(percentage/2),end = "")
                # print( f"\r\x1b[71C]",end = "")
                print(f"\t {i} of {file_number}",end ="")
                print("\r",end = "")


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Eduscope Video Downloader (v.1.0.0)')
        self.geometry('680x200')
        self.resizable(0, 0)

        self.create_header_frame()
        self.create_body_frame()
        self.create_footer_frame()

    def create_header_frame(self):

        self.header = ttk.Frame(self)
        # configure the grid
        self.header.columnconfigure(0, weight=1)
        self.header.columnconfigure(1, weight=10)
        self.header.columnconfigure(2, weight=1)
        # label
        self.label = ttk.Label(self.header, text='URL')
        self.label.grid(column=0, row=0, sticky=tk.W)

        # entry
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(self.header,
                                   textvariable=self.url_var,
                                   width=80)

        self.url_entry.grid(column=1, row=0, sticky=tk.EW)

        # download button
        self.download_button = ttk.Button(self.header, text='Download')
        self.download_button['command'] = self.handle_download
        self.download_button.grid(column=2, row=0, sticky=tk.E)

        # attach the header frame
        self.header.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

    def handle_download(self):
        link = self.url_var.get()

        file_path = "https://lecturecapture.sliit.lk/archive/saved/Personal_Capture/"
        if(len(link) == 68):
            ID = link[-23:] + "&full=ZnVsbA%3D%3D"
        else:
            ID = link.replace("https://lecturecapture.sliit.lk/neplayer.php?", "")

        MAIN_URL = "https://lecturecapture.sliit.lk/webservice.php?key=vhjgyu456dCT&type=video_paths&"
        URL = MAIN_URL + ID

        session = requests.Session()

        response = session.get(URL).text
        # print(response)
        data =json.loads(response)
        

        video_path_prefix = data['video_1_m3u8_list']

        video_path_postfix = video_path_prefix.replace(
            "../../archive/saved/Personal_Capture/", "")
        main_path = file_path+video_path_postfix.replace(".m3u8", "")+"_144.m3u8"

        self.download_button['state'] = tk.DISABLED
        download_thread = AsyncDownload(main_path)
        download_thread.start()
        self.monitor(download_thread)
        self.html.delete(1.0 ,tk.END)
        self.html.insert(1.0 , "Downloading")
    def monitor(self, thread):
        
        if thread.is_alive():
            # check the thread every 100ms
            self.html.insert(1.0 , "=" , tk.FIRST)
            self.after(100, lambda: self.monitor(thread))
        
        else:

            self.msg = messagebox.showinfo('Eduscope Downloader' , "Download Finished..!")
            self.html.delete(1.0 ,tk.END)
            # self.html.insert(1.0 , "Download finished..")            
            self.html.insert(1.0, "1.Go to the Eduscope Page\n2.Copy the link in address bar\n3.Just paste in this url bar\n4.simply hit to download\n5.Video will available in same applicaiton directory")
            self.download_button['state'] = tk.NORMAL
            self.url_entry.delete(0 , tk.END)


    def create_body_frame(self):
        # pass
        self.body = ttk.Frame(self)
        # text and scrollbar
        self.html = tk.Text(self.body, height=5)
        self.html.grid(column=0, row=1)
        self.html.insert(1.0, "1.Go to the Eduscope Page\n2.Copy the link in address bar\n3.Just paste in this url bar\n4.simply hit to download\n5.Video will available in same applicaiton directory")
        # self.progressBar = ttk.Progressbar(self.body, orient="horizontal" , length=500)
        # self.progressBar.grid(column=0, row=1)
        scrollbar = ttk.Scrollbar(self.body,
                                  orient='vertical',
                                  command=self.html.yview)

        scrollbar.grid(column=1, row=1, sticky=tk.NS)
        self.html['yscrollcommand'] = scrollbar.set
        
        self.body.grid(column=0, row=1, sticky=tk.NSEW, padx=10, pady=10)

    def create_footer_frame(self):
        self.footer = ttk.Frame(self)
        # configure the grid
        self.footer.columnconfigure(0, weight=1)
        # exit button
        self.exit_button = ttk.Button(self.footer,
                                      text='Exit',
                                      command=self.destroy)

        self.exit_button.grid(column=0, row=0, sticky=tk.E)

        # attach the footer frame
        self.footer.grid(column=0, row=2, sticky=tk.NSEW, padx=10, pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
