"""Initializing app."""

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

Base = declarative_base()
engine = create_engine("sqlite:///taxi_data.db")
Session = sessionmaker(bind=engine)
session = Session()

from app import views
