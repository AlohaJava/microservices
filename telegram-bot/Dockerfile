FROM python:3.6

ADD 79885430081.session /
RUN pip install quart
RUN pip install telethon
RUN pip install psycopg2-binary

ADD app.py /
ADD db.py /
ADD bot.py /

CMD [ "python", "./app.py" ]