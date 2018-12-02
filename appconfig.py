from flask import Flask
from peewee import PostgresqlDatabase

UPLOAD_FOLDER = 'content'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['PREV_FOLDER'] = ''

psql_db = PostgresqlDatabase(
    'backend',
    user='backend',
    password='backend',
    host='127.0.0.1')
