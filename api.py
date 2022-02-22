from sqlalchemy import extract
from db import engine
from db_schema import Episode, episode_subjects, painting_colors
from flask import Flask, jsonify, request
from sqlalchemy.orm import scoped_session, sessionmaker
import pandas as pd
import urllib
import os

app = Flask(__name__)

sess_factory = sessionmaker(bind=engine, expire_on_commit=False)
session = scoped_session(sess_factory)

STAGING_ROOT = os.path.join(os.getcwd(), 'staging')


@app.route("/")
def getList():
    """ getList - returns a list of episodes based on filters """
    page = request.args.get('page', 1)
    perPage = request.args.get('perPage', 10)
    month = request.args.get('month')
    subjects = request.args.get('subjects')
    colors = request.args.get('colors')
    q = session.query(Episode)
    if month:
        q = q.filter(extract('month', Episode.date) == month)
    if subjects:
        subjects = urllib.parse.unquote(subjects).split(',')
        sub_stmt = session.query(episode_subjects.columns.episode_id).filter(
            episode_subjects.columns.subject_id.in_(subjects))
        q = q.filter(Episode.id.in_(sub_stmt))
    if colors:
        colors = urllib.parse.unquote(colors).split(',')
        sub_stmt = session.query(painting_colors.columns.episode_id).filter(
            painting_colors.columns.color_id.in_(colors))
        q = q.filter(Episode.id.in_(sub_stmt))
    q = q.offset(page - 1 * perPage).limit(perPage)
    print(q.statement)
    return jsonify([episode.toDict() for episode in q.all()][:1])


if __name__ == '__main__':
    print("Loading database from staging files...")
    df = pd.read_csv(os.path.join(STAGING_ROOT, 'episodes.csv'))
    df.to_sql('episodes', con=engine, if_exists='replace')
    print(f" Eposodes loaded: {len(df.index)}")
    df = pd.read_csv(os.path.join(STAGING_ROOT, 'colors.csv'))
    df.to_sql('colors', con=engine, if_exists='replace')
    print(f" Colors loaded: {len(df.index)}")
    df = pd.read_csv(os.path.join(STAGING_ROOT, 'subjects.csv'))
    df.to_sql('subjects', con=engine, if_exists='replace')
    print(f" Subjects loaded: {len(df.index)}")
    df = pd.read_csv(os.path.join(STAGING_ROOT, 'episode_colors.csv'))
    df.to_sql('episode_colors', con=engine, if_exists='replace')
    print(f" Eposode colors loaded: {len(df.index)}")
    df = pd.read_csv(os.path.join(STAGING_ROOT, 'episode_subjects.csv'))
    df.to_sql('episode_subjects', con=engine, if_exists='replace')
    print(f" Eposode subjects loaded: {len(df.index)}")
    print("Database loaded!")
    app.run()
    print("Ready to go!")
