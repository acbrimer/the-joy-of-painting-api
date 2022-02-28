from sqlalchemy import extract
from sqlalchemy.orm import scoped_session, sessionmaker
from db import engine
from db_schema import Base, Episode, episode_subjects, painting_colors
from flask import Flask, jsonify, request
import urllib
import os
import json

app = Flask(__name__)

session = scoped_session(sessionmaker(bind=engine))


@app.teardown_request
def remove_session(ex=None):
    session.remove()


@app.route("/tables")
def getTables():
    return jsonify(dict({"tables": list(Base.metadata.tables.keys())}))


@app.route("/testdata")
def testData():
    try:
        with open(os.path.join(os.getcwd(), "testdata.json"), 'r') as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": "could not open file"})


@app.route("/")
def getList():
    """ getList - returns a list of episodes based on filters """
    page = request.args.get('page', 1)
    if (isinstance(page, str)):
        try:
            page = int(page)
        except Exception as e:
            page = 1
    perPage = request.args.get('perPage', 10)
    print(f"perPage: {perPage}")
    if (isinstance(perPage, str)):
        try:
            perPage = int(perPage)
        except Exception as e:
            perPage = 10
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
    return jsonify([episode.toDict() for episode in q.all()])


if __name__ == '__main__':
    print('runApp')
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))
