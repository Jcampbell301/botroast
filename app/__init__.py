import flask
import json
from flask import request
from bot import Bot
import requests
from flask import flash, redirect
from forms import RegisterForm
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views