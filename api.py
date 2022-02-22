from sqlalchemy import extract
from db import engine
from db_schema import Episode, Color, Subject
from flask import Flask, jsonify, request
from sqlalchemy.orm import scoped_session, sessionmaker
import pandas as pd
import os

app = Flask(__name__)

sess_factory = sessionmaker(bind=engine, expire_on_commit=False)
session = scoped_session(sess_factory)

STAGING_ROOT = os.path.join(os.getcwd(), 'staging')

@app.route("/")
def getList():
    """ getList - returns a list of episodes based on filters """
    month = request.args.get('month')
    subjects = request.args.get('subjects')
    colors = request.args.get('colors')
    q = session.query(Episode)
    if month:
        q.filter(extract('month', Episode.date))

    return jsonify(q.all())


if __name__ == '__main__':
    print("Loading database from staging files...")
    df = pd.read_csv(os.path.join(STAGING_ROOT, 'episodes'))
    df.to_sql('episodes', con=engine)
    print(f" Eposodes loaded: {len(df.index)}")
    df = pd.read_csv(os.path.join(STAGING_ROOT, 'colors'))
    df.to_sql('colors', con=engine)
    print(f" Colors loaded: {len(df.index)}")
    df = pd.read_csv(os.path.join(STAGING_ROOT, 'subjects'))
    df.to_sql('subjects', con=engine)
    print(f" Subjects loaded: {len(df.index)}")
    df = pd.read_csv(os.path.join(STAGING_ROOT, 'episode_colors'))
    df.to_sql('episode_colors', con=engine)
    print(f" Eposode colors loaded: {len(df.index)}")
    
