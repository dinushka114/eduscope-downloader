import requests
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys 
import time
import sys
import m3u8
import subprocess
from os import path
import os

sys.tracebacklimit=0
print(

	'''
            (           (           )  (         
            )\ )        )\ )  (  ( /(  )\ )      
         ( (()/(     ( (()/(  )\ )\())(()/((     
         )\ /(_))    )\ /(_)|((_|(_)\  /(_))\    
        ((_|_))_  _ ((_|_)) )\___ ((_)(_))((_)   
        | __|   \| | | / __((/ __/ _ \| _ \ __|  
        | _|| |) | |_| \__ \| (_| (_) |  _/ _|   
        |___|___/ \___/|___/ \___\___/|_| |___| 

 (        )             ) (       )       (         (    
 )\ )  ( /( (  (     ( /( )\ ) ( /(  (    )\ )      )\ ) 
(()/(  )\()))\))(   ')\()|()/( )\()) )\  (()/(  (  (()/( 
 /(_))((_)\((_)()\ )((_)\ /(_)|(_)((((_)( /(_)) )\  /(_))
(_))_   ((_)(())\_)()_((_|_))   ((_)\ _ )(_))_ ((_)(_))  
 |   \ / _ \ \((_)/ / \| | |   / _ (_)_\(_)   \| __| _ \ 
 | |) | (_) \ \/\/ /| .` | |__| (_) / _ \ | |) | _||   / 
 |___/ \___/ \_/\_/ |_|\_|____|\___/_/ \_\|___/|___|_|_\ 

by D I N U S H K A P I Y U M A L
	'''

	)

if(path.exists("data.dat")):
    userData = open("data.dat" , "r")
    ed_email = userData.readline()
    ed_pass = userData.readline()
else:
    userData = open("data.dat" , "w")
    ed_email = input("Enter student email correctly: ")
    ed_pass = input("Enter password correctly: ")
    userData.write(ed_email+"\n")
    userData.write(ed_pass)


eduscope_link = input("Enter URL to download: ")

eduscope_link = eduscope_link.lstrip(" ")
eduscope_link = eduscope_link.rstrip(" ")

driver = webdriver.Chrome('./chromedriver')  
driver.get(eduscope_link) 


username = driver.find_element_by_name("inputEmail")
username.send_keys(ed_email)
time.sleep(1)
password = driver.find_element_by_name("inputPassword")
password.send_keys(ed_pass)

btn = driver.find_element_by_name('submit')
btn.click()

time.sleep(10)

# x =  requests.get(url)

reqlist = []
for request in driver.requests:
    if request.response:
        reqlist.append(request.url)

link = reqlist[-1]
for l in reqlist:
	if(l[-4:]=="m3u8" or l[-2:]=="ts"):
		link = l

if(link[-2:]=="ts"):
	link = link.rstrip(link[-8:])+".m3u8"

# print(link)
driver.close()

char = ''
link_length = len(link)
count= link_length -1
url_cmp = ""
for i in range(link_length):
	char = link[count]
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


url_info = link.replace(fileNameInUrl , " ")
url_cmp = fileNameInUrl.lstrip("/")

url_info = url_info.rstrip(" ")+"/"
# print(url_info)
# print(url_cmp)
file_name = url_cmp.rstrip(".m3u8")
url_1 = url_info + url_cmp

r_1 = requests.get(url_1)

m3u8_master = m3u8.loads(r_1.text)

file_number = 0
i = 0
percentage = 0.0
print(" ")
print(f'---------------Downloading started {file_name} --------------')
print('')
for segment in m3u8_master.data['segments']:
    file_number += 1

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
        print( f"{(str(percentage))[0:5]} %",end = "")
        print("\r\x1b[20C[",end = "")
        print( f"="*int(percentage/2),end = "")
        print( f"\r\x1b[71C]",end = "")
        print(f"\t {i} of {file_number}",end ="")
        print("\r",end = "")


print("\n")
print("Downlaod finished....")
print("Converting file in progress.....")


infile = file_name+".ts"
outfile = file_name+".mp4"
subprocess.run(['ffmpeg' , '-i' , infile , outfile])
os.remove(file_name+".ts")

