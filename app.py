import streamlit as st
import os
from pytube import YouTube

@st.cache_resource
def installff():
  os.system('sbase install geckodriver')

_ = installff()
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from pytube import YouTube
from moviepy.editor import *
import sys
import os
import re
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from zipfile import ZipFile
from zipfile import ZIP_BZIP2


def getLinks():
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(options=opts)
    print('opening_browser')

    ytUrl=str('https://www.youtube.com/results?search_query=')+artistName+" songs"
    
    browser.get(ytUrl)


    time.sleep(15)

    listElem=browser.find_elements('xpath','//a[@id="thumbnail"]') ## only pick n links
    addrs=[]
    for x in listElem:
        addrs.append(x.get_attribute('href'))
    
    download_songs(n,addrs,nsec)

def download_songs(n,addrs,nsec):
    downloadList=[]
    nc=int(n)
    i = 0
    for x in addrs:
        if x==None :
            continue
        yt=YouTube(x)
        print(yt)
        # print(f"link : {yt.length}")
        if yt.length >= 120 and yt.length <= 360 :
            yt.streams.get_audio_only().download(filename = str(i)+'.mp3')
            print(yt.title+" has been succesfully downloaded! ")
            downloadList.append(str(i)+'.mp3')
            i += 1
            nc=nc-1
            if nc<=0:
                break
    createFinalMashup(downloadList,nsec)
    
def createFinalMashup(downloadList,nsec):
    allsongs=[]
    for s in range(len(downloadList)-1):
        currSong=AudioFileClip(downloadList[s])
        #  currSong=currSong.cutout(int(nsec),currSong.duration)
        currSong = currSong.subclip(0,nsec)
        allsongs.append(currSong)
    finalAudio=concatenate_audioclips(allsongs)
    finalAudio.write_audiofile('output.mp3')
    with ZipFile(f'Mashup.zip','w',compression= ZIP_BZIP2 , allowZip64=True, compresslevel=9) as zip:
          zip.write('output.mp3')
    for x in allsongs:
        x.close()
    deleteFiles(downloadList)

def deleteFiles(downloadList):
    for x in downloadList:
        os.remove(x)    

def send_email(mailid) :
    data.write('Sending email....')
    fromaddr = "mashedupbyprianshu@gmail.com"
    toaddr = mailid
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Mashup"
    body = "Enjoy your mashup :) "
    msg.attach(MIMEText(body, 'plain'))
    attachment = open('Mashup.zip', "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
  
    encoders.encode_base64(p)
   
    p.add_header('Content-Disposition', "attachment; filename= %s" % "mashup.zip")
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(fromaddr, 'sxaiyxxwtrdrqqyh')
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

    data.empty()
    st.info('process completed')

st.title('Mashedup- Mashup songs from your fav artists')

st.write('Enter name of your favourite singer, number of songs, amount of song to trim and you will reveive a mashup through your email')

with st.form('input') :
    singername = st.text_input('Enter singer name')

    numSongs = st.text_input('Enter number of songs')

    y = st.text_input('Enter length of each song')

    email = st.text_input('Enter your email')

    submit_button = st.form_submit_button(label='Submit')

data = st.empty()

if submit_button :
    if singername != '' and numSongs != '' and y != '' and email != '' :
        artistName = singername.split()[0]
        n = numSongs.split()[0]
        nsec = y.split()[0]
        email = email.split()[0]
        regex = '[A-Za-z0-9_]*@[A-Za-z]*\.[A-Za-z]*'
        match = re.findall(regex,email)
        if match[0] != email :
            st.error('Wrong email')
        else :
            # try :
            nsec = int(nsec)
            n = int(n)
            getLinks()
            send_email(email)
            # except :
                # st.error('Invalid input type entered!!')
    else :
        st.error('Please enter data in all fields')