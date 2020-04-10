#! /usr/bin/env python
# coding=utf-8

import sys
import datetime as dt
import time
import smtplib
from chain import password
from chain import text as body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

sender = 'zplacesound@gmail.com'
fmt = 'From: {}\r\nTo: {}\r\nSubject: {}\r\n{}'

def send_email():
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('zplacesound@gmail.com', password)
	msg = MIMEMultipart()
	msg['To'] = sender
	msg['From'] = sender
	msg['Subject'] = "Добро пожаловать в реальный мир"
	msg.attach(MIMEText(body, 'html', _charset='utf-8'))
	text = msg.as_string()
	server.sendmail(sender, sender, text)
	server.quit()

send_email()
