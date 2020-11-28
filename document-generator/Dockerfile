FROM python:3.6

RUN pip install flask
RUN pip install psycopg2-binary

ADD app.py /
ADD 1.docx /

CMD [ "python", "./app.py" ]