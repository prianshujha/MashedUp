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


    time.sleep(20)

    listElem=browser.find_elements('xpath','//a[@id="thumbnail"]') ## only pick n links
    addrs=[]
    for x in listElem:
        addrs.append(x.get_attribute('href'))
    filtered_addr = filter(lambda item: item is not None, addrs)
    addrs = list(filtered_addr)
    download_songs(n,addrs,nsec)

def download_songs(n,addrs,nsec):
    downloadList=[]
    nc=int(n)
    i = 0
    for x in addrs:
        if x==None :
            continue
        try :
            yt=YouTube(x)
            print(yt)
        # print(f"link : {yt.length}")
            if yt.length >= 120 and yt.length <= 360 :
                if yt.length<nsec:
                    continue
                yt.streams.get_audio_only().download(filename = str(i)+'.mp3')
                print(yt.title+" has been succesfully downloaded! ")
                downloadList.append(str(i)+'.mp3')
                i += 1
                nc=nc-1
                if nc<=0:
                    break
        except :
            print('error')
            
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
    st.info('Hang tight! Creating final Mashup...')

def deleteFiles(downloadList):
    for x in downloadList:
        os.remove(x)    

def send_email(mailid,artistName) :
    data.write('Sending email....')
    fromaddr = "mashedupbyprianshu@gmail.com"
    toaddr = mailid
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Mashup of "+ artistName
    body = "Here's your mashup of "+artistName
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
    st.info('Enjoy Your Mashup!')

st.title('Mashedup- Mashup songs from your fav artists')

st.write('Here are steps to get the mashup of your favourite artist: ')
st.write(' 1. Fill in the Artist Name ')
st.write(' 2. Fill in the number of Songs to pick for mashup ')
st.write(' 3. Fill in the duration of each song ')
st.write(' 4. Fill in the email for the mashup to be delivered ')
st.write(' 5. & thats all,  you\'ll have the mashup delevered to your inbox in minutes \n')

with st.form('input') :
    singername = st.text_input('Artist Name')

    numSongs = st.text_input('Number of songs')

    y = st.text_input('Duration of each song')

    email = st.text_input('Email')

    submit_button = st.form_submit_button(label='Submit')

data = st.empty()

if submit_button :
    if singername != '' and numSongs != '' and y != '' and email != '' :
        artistName = singername.split()[0]
        n = numSongs.split()[0]
        nsec = y.split()[0]
        email = email.split()[0]
        regex = '[A-Za-z0-9._]*@[A-Za-z]*\.[A-Za-z]*'
        match = re.findall(regex,email)
        if match[0] != email :
            st.error('Wrong email')
        else :
            try :
                nsec = int(nsec)
                n = int(n)
            except :
                st.error('Invalid input type entered!!')
            # try:
            with st.spinner(text='This may take a minute or two !'):
                time.sleep(5)
                try:
                  getLinks()
                 except:
                  st.error('Uh, Oh...The server seems to be busy, but you can surely comeback later :)')
                send_email(email,singername)
                st.success('Done')
            
            # except:
                # st.error('Uh Oh, Sometimes the server is busy, but you can surely comeback later!')
            

            # except:
            # st.error('Server busy, Please try again Later!')
    else :
        st.error('Please enter data in all fields')
