import requests
import json
import m3u8
import subprocess
from os import path
import os
global file_path

file_path = "https://lecturecapture.sliit.lk/archive/saved/Personal_Capture/"


print("""

	 /$$$$$$$$ /$$$$$$$   /$$$$$$  /$$      /$$ /$$   /$$
	| $$_____/| $$__  $$ /$$__  $$| $$  /$ | $$| $$$ | $$
	| $$      | $$  \ $$| $$  \ $$| $$ /$$$| $$| $$$$| $$
	| $$$$$   | $$  | $$| $$  | $$| $$/$$ $$ $$| $$ $$ $$
	| $$__/   | $$  | $$| $$  | $$| $$$$_  $$$$| $$  $$$$
	| $$      | $$  | $$| $$  | $$| $$$/ \  $$$| $$\  $$$
	| $$$$$$$$| $$$$$$$/|  $$$$$$/| $$/   \  $$| $$ \  $$
	|________/|_______/  \______/ |__/     \__/|__/  \__/
    	By-: DINUSHKA PIYUMAL

    			  Enter URL here
			          .
			      . ;.
			       .;
			        ;;.
			      ;.;;
			      ;;;;.
			      ;;;;;
			      ;;;;;
			      ;;;;;
			      ;;;;;
			      ;;;;;
			    ..;;;;;..
			     ':::::'
			       ':`

	""")

def get_actual_path():
	link = input("Enter url for downlaod:")

	if(len(link)==68):
		ID = link[-23:] + "&full=ZnVsbA%3D%3D"
	else:
		ID = link.replace("https://lecturecapture.sliit.lk/neplayer.php?","")

	MAIN_URL = "https://lecturecapture.sliit.lk/webservice.php?key=vhjgyu456dCT&type=video_paths&"
	URL = MAIN_URL + ID

	session = requests.Session()

	response = session.get(URL).text

	data = json.loads(response)

	video_path_prefix = data['video_1_m3u8_list']

	video_path_postfix = video_path_prefix.replace("../../archive/saved/Personal_Capture/" , "")
	main_path = file_path+video_path_postfix.replace(".m3u8" , "")+"_144.m3u8"
	# print(main_path)
	return main_path

def download_video(main_path):
	char = ''
	main_path_length = len(main_path)
	count= main_path_length -1
	url_cmp = ""
	for i in range(main_path_length):
		char = main_path[count]
		url_cmp+=char
		if(char=="/"):
			break
		count-=1
	fileNameInUrl = "";
	count_file_name = len(url_cmp) -1
	while(count_file_name>=0):
		fileNameInUrl+=url_cmp[count_file_name]
		count_file_name-=1
	file_path="./"
	url_info = main_path.replace(fileNameInUrl , " ")
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

	# progress_bar.close()
	print("\n")
	print("Downlaod finished....")
	return file_name


def convert(file_name):
	print("Start converting........")
	infile = file_name+".ts"
	outfile = file_name+".mp4"
	subprocess.run(['ffmpeg' , '-i' , infile , outfile])
	os.remove(file_name+".ts")
	print("Sucessfully download and convert file........")
if __name__ == '__main__':
	path = get_actual_path()
	file = download_video(path)
	convert(file)
