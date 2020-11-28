import os
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase

import psycopg2
from flask import Flask, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage

app = Flask(__name__)
fromaddr = "notifier-bot-rosseti@mail.ru"
mypass = "ZakaerSter1221Al$"


@app.route('/')
def hello_world():
    return 'Hello World!'


def get_connection():
    conn = psycopg2.connect(dbname='postgres', user='postgres',
                            password='example', host='db')
    return conn


def insert_to_db(subject, body, to, file):
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("INSERT INTO email_messages(from_email,to_email,subject,message,file) VALUES('{0}','{1}','{2}','{3}','{4}')".format(fromaddr,to,subject,body,file))


def send_email(subject, body, to, file):
    try:
        print("Sending email to:" + to)
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        server.login(fromaddr, mypass)
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['Subject'] = subject
        msg['To'] = to
        file.save(file.filename)
        msg.attach(MIMEText(body))

        part = MIMEApplication(
            open(file.filename, 'rb').read(),
            Name=file.filename
        )

        part['Content-Disposition'] = 'attachment; filename="%s"' % file.filename
        msg.attach(part)
        server.send_message(msg)
        os.remove(file.filename)
        insert_to_db(subject, body, to, file.filename)
        return "ok"
    except Exception:
        return "Server Error!"


@app.route("/sendemail", methods=["POST"])
def do_something():
    form = request.form
    print(form['subject'] + " " + form['body'] + " " + form['to'])
    return send_email(form['subject'], form['body'], form['to'], request.files['file'])
    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
