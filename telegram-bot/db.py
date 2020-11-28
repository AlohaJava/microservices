
import psycopg2


def get_connection():
    conn = psycopg2.connect(dbname='postgres', user='postgres',
                            password='example', host='db')
    return conn


def get_chat_id(topic):
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("select telegram_chat_id from topics where name='" + topic + "'")
        records = cursor.fetchall()
        return records[0][0]


def update_chat_id(topic_name, telegram_chat_id):
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("update topics set telegram_chat_id={0} where name='{1}'".format(telegram_chat_id, topic_name))


