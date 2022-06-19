from genericpath import exists
import cv2
import datetime
import time
import os
from gtts import gTTS
from playsound import playsound

today_day = datetime.date.today().day
today_month = datetime.date.today().month
today_year = datetime.date.today().year

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

name = input('What is your name ?\n')

video_recorder = cv2.VideoCapture(0)

ret, frame = video_recorder.read()

image_folders = os.listdir('./img/')
sound_folders = os.listdir('./sound/')

image_folder_res = name in image_folders
sound_folders_res = name in sound_folders

def Text_to_speech(name_to_speak):
    speech = gTTS("Bonjour " + name_to_speak, lang="fr")
    speech.save('./sound/'+name_to_speak+'/'+'Bonjour.mp3')
    playsound('./sound/'+name_to_speak+'/'+'Bonjour.mp3')


while True:
    cv2.imshow('img',frame)
    if cv2.waitKey(1) & 0xFF == ord('y'):
        if(not(image_folder_res)):
            print('Creating folder in ./img')
            print('Folder ./img/'+name+' created')
            os.mkdir('./img/'+name)
        if(not(sound_folders_res)):
            print('Creating folder in ./sound')
            print('Folder ./sound/'+name+' created')
            os.mkdir('./sound/'+name)
        cv2.imwrite('./img/'+name+'/'+str(today_day)+'-'+str(today_month)+'-'+str(today_year)+'_'+current_time+'.png', frame)
        Text_to_speech(name)
        cv2.destroyAllWindows()
        break
    

video_recorder.release()
