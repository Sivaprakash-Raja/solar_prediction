import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import date

import pandas as pd


def sendmail(file_path,pred_path,mail_path):

	predicted = pd.read_csv(pred_path)
	actual = pd.read_csv(file_path)

	data = {"date":actual.date,"time":actual.time,"actual_temp":actual.temp,"actual_solar":actual.solar_irradiation,"timef":predicted.time,"predicted_temp":predicted.temperature,"predicted_solar":predicted.solar_predict}

	df = pd.DataFrame(data,columns =['date','time','actual_temp','actual_solar','timef','predicted_temp','predicted_solar'])
	file_name = f'{str(date.today())}.csv'

	df.to_csv(path = mail_path+file_name , index = False)
	
	fromaddr = "svquants@gmail.com"
	toaddr = "svprakash1310@gmail.com"
	   
	# instance of MIMEMultipart
	msg = MIMEMultipart()
	  
	# storing the senders email address  
	msg['From'] = fromaddr
	  
	# storing the receivers email address 
	msg['To'] = toaddr
	  
	# storing the subject 
	msg['Subject'] = "Subject of the Mail"
	  
	# string to store the body of the mail
	body = "Body_of_the_mail"
	  
	# attach the body with the msg instance
	msg.attach(MIMEText(body, 'plain'))
	  
	# open the file to be sent 
	filename = "rtest.csv"
	attachment = open( mail_path+file_name, "rb")
	  
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
	s.login(fromaddr, "qazplm10")
	  
	# Converts the Multipart msg into a string
	text = msg.as_string()
	  
	# sending the mail
	s.sendmail(fromaddr, toaddr, text)
	  
	# terminating the session
	s.quit()
	print("mail sent")

