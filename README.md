# MashedUp- Mashup Songs from Your favourite artist

## App Description
This is a web application, deployed on Streamlit. It creates mashup of the user specified artist and gets the mashup delivered to your mail.
https://prianshujha-mashedup-app-6ldlqc.streamlit.app/

## Streamlit
Streamlit has been used to deploy this webapp. The ```app.py``` file is the deployment module for the web application.

## Selenium
Selenium has been used to perform YouTube search of the user specified artist.

## Pytube
Pytube has been used to retrieve audio from the collected youtube links

## Moviepy 
Moviepy has been used to trim and mix the audio as specified by the user

## Smtplib
Smtplib has been used to send the mashup file through mail to the user
