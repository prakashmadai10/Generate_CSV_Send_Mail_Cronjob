from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import time
import pandas as pd
import openpyxl
from schedule_tasks.extract_from_database import *
from datetime import datetime
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate
from email import encoders
import os  


scheduler = BackgroundScheduler()


def sync_date():
    today = pd.to_datetime("today").strftime('%Y_%m_%d')
    return today


@scheduler.scheduled_job('cron', hour='21', minute='22', misfire_grace_time=60)
def test_scheduler_generate_csv():
    dt_format = sync_date()
    
    print("Sync Started at", sync_date())
    df = extract_data_db_dataframe()
    writer = pd.ExcelWriter('{0}.xlsx'.format('Data from Postgres DB_'+dt_format))
    df.to_excel(writer, sheet_name='Sheet1',
                index=False, na_rep='0')
    
    #Auto-Adjust the Width of Excel Columns
    for column in df:
        column_length = max(df[column].astype(
            str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['Sheet1'].set_column(
            col_idx, col_idx, column_length)
    writer.save()

    print("-------Dump Generation COMPLETED ---------")
    return 0

@scheduler.scheduled_job('cron', hour='21', minute='38', misfire_grace_time=60)
def send_excel_attachment_mail():
    '''
Steps to Send Mail with attachments using SMTP (smtplib)
1.Create MIME
2.Add sender, receiver address into the MIME
3.Add the mail title into the MIME
4.Attach the body,image,attachments into the MIME
5.Start the SMTP session with valid port number with proper security features.
6.Login to the system.
7.Send mail and exit
    '''
   
    print("Sync Started at", sync_date())
    dt_format = sync_date()

    #attach generated CSV
    wb_path='{0}.xlsx'.format('Data from Postgres DB_'+dt_format)
        
    msg = MIMEMultipart()
    sender_pass = 'xxxxxx'

    to = "test1@gmail.com"
    from1 ='test2@gmail.com'
    cc = 'test3@gmail.com'
    msg['From'] = from1
    msg['To'] = to
    msg['Cc'] = cc
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'Latest Data from Postgres DB'
    msg.attach(
        MIMEText("""<p>Dear Sir/Madam</p> <p>Please find the attachment</p><p>Regards<p>Prakash Singh Madai<br>
(ISO 27001:2013 Certified Company)<br>
2nd Floor, DD Plaza, Santa Marg, Kamaladi,<br>
PO Box: 21400, Kathmandu, Nepal<br>
Tel: +977-1-4255306  Ext. 106<br>
Fax: +977-1-4255309<br>
<img src="cid:sign" alt="some error" width="600" height="309">
""", 'html'))

    fp = open('Scheduler\\sign.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<sign>')
    msg.attach(msgImage)

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(wb_path, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                    'attachment', filename='Latest Data from Postgres DB'+dt_format+'.xlsx')
    msg.attach(part)
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(from1, sender_pass) #login with mail_id and password

    smtp.ehlo()
    smtp.sendmail(msg['From'], [msg['To'], msg['Cc']], msg.as_string())
    smtp.quit()
    print("Mail Successfully Sent")


