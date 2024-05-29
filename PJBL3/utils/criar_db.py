from flask import Flask
from modelos import *

def criar_db(app:Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()