import json

from flask import Flask, request
import psycopg2


def get_connection():
    conn = psycopg2.connect(dbname='postgres', user='postgres',
                            password='example', host='84.201.137.231')
    return conn


def get_suggestions_for_topics(topic):
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("select name from topics where name LIKE '%{0}%'".format(topic))
        records = cursor.fetchall()
        results = []
        for res in records:
            results.append(res[0])
        return json.dumps(results)


def get_suggestions_for_users(topic):
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("select full_name from users where full_name LIKE '%{0}%'".format(topic))
        records = cursor.fetchall()
        results = []
        for res in records:
            results.append(res[0])
        return json.dumps(results)


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/get_suggestion_topics', methods=['POST'])
def get_suggestion():
    data = request.json
    return get_suggestions_for_topics(data['text'])


@app.route('/get_suggestion_users', methods=['POST'])
def get_suggestion2():
    data = request.json
    return get_suggestions_for_users(data['text'])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
