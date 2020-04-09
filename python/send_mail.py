import datetime as dt
import time
import smtplib
from chain import password

def send_email():
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('zplacesound@gmail.com', password)
	message = """<div dir="ltr"><div>So long, and thanks for all the fish!<br><br></div>-Al<br></div>\r\n"""
	server.sendmail('zplacesound@gmail.com', 'zplacesound@gmail.com', message)
	server.quit()

send_email()
