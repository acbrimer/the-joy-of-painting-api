from models.db_schema import Episode
from models import storage
import pandas as pd
from pandas import DataFrame
import os
from typing import Type, List
import pandas as pd
import os


DATA_ROOT = os.path.join(os.getcwd(), 'data')


df_colors = pd.read_csv(os.path.join(
    DATA_ROOT, 'The Joy Of Painiting - Colors Used'))
df_colors['TITLE'] = df_colors.apply(
    lambda r: r['painting_title'].upper(), axis=1)
df_colors['EPISODE'] = df_colors.apply(
    lambda r: f"S{r['season']:02}E{r['episode']:02}", axis=1)

df_subjects = pd.read_csv(os.path.join(
    DATA_ROOT, 'The Joy Of Painiting - Subject Matter'))
# update column - remove surrounding quotes from TITLE
df_subjects['TITLE'] = df_subjects.apply(lambda r: r['TITLE'][1:-1], axis=1)

df_dates = pd.read_csv(os.path.join(
    DATA_ROOT, 'The Joy Of Painting - Episode Dates'), delimiter="\t", header=None, names=['src'])

# parse df_dates (not actually CSV-- parse each row of file as col in df)
df_dates['date'] = df_dates.apply(
    lambda r: r['src'][r['src'].find('(')+1:r['src'].find(')')].strip(), axis=1)
df_dates['title'] = df_dates.apply(
    lambda r: r['src'].split(r['date'])[0][:-1].strip(), axis=1
)
df_dates['note'] = df_dates.apply(
    lambda r: r['src'].split(r['date'])[1][1:-1].strip(), axis=1
)
df_dates['TITLE'] = df_dates.apply(lambda r: r['title'].upper(), axis=1)

# get complete TITLE -> EPISODE xwalk from union of matches in df_colors/df_subjects


df_titles = pd.concat([df_colors[['TITLE', 'EPISODE']],
                      df_subjects[['TITLE', 'EPISODE']]])
# drop missing matches
df_titles.dropna(inplace=True)
# drop duplicates
df_titles.drop_duplicates(inplace=True)

# show missing titles


def getDatesForTitles(r):
    xwalk = {
        'EVERGREENS AT SUNSET': 'EVERGREEN AT SUNSET',
        'MOUNTAIN PATH': 'MOUNTAIN PASS',
        'SHADES OF GREY': 'SHADES OF GRAY',
        'EVENING AT SUNSET': 'EVENING SUNSET',
        'HALF-OVAL VIGNETTE': 'HALF OVAL VIGNETTE',
        'OLD OAK TREE': 'THE OLD OAK TREE',
        'GRAY MOUNTAIN': 'GREY MOUNTAIN',
        'THE OLD HOME PLACE': 'OLD PLACE HOME',
        'WOODMAN\'S RETREAT': 'WOODSMAN\'S RETREAT',
    }
    title = r['TITLE']
    if title in xwalk:
        title = xwalk[title]
    matches = df_dates.loc[df_dates['TITLE'].str.contains(title)]
    if matches.empty:
        return None
    return matches.iloc[0]['date']


def getEpisodeForDate(r):
    date = r['date']
    title = r['TITLE']
    if date:
        matches = df_titles.loc[df_titles['date'] == date]
        if not matches.empty:
            return matches.iloc[0]['EPISODE']
    if title:
        matches = df_titles.loc[df_titles['TITLE'].str.contains(title)]
        if not matches.empty:
            return matches.iloc[0]['EPISODE']
    return None


df_titles['date'] = df_titles.apply(getDatesForTitles, axis=1)
df_dates['EPISODE'] = df_dates.apply(getEpisodeForDate, axis=1)
# hardcoding this last pain in the add ID
df_dates.at[264, 'EPISODE'] = 'S21E05'
# this should return nothing
df_dates.loc[df_dates['EPISODE'].isnull()]


class EpisodeLoader(Episode):

    @classmethod
    def load(cls):
        # new df with EPISODE, TITLE from df_subjet_matter
        df = df_dates[['EPISODE', 'title', 'date', 'note']]
        # new column - season number from EPISODE string
        df['season'] = df.apply(
            lambda r: int(r['EPISODE'].split('E')[0][1:]), axis=1)
        # new column - episode number from EPISODE string
        df['episode'] = df.apply(
            lambda r: int(r['EPISODE'].split('E')[1][1:]), axis=1)
        # rename columns
        df.rename(columns={"EPISODE": "id"}, inplace=True)
        # update column order
        df = df[['id', 'season', 'episode', 'title', 'date', 'note']]

        df.to_sql(cls.__tablename__, con=storage.engine)


if __name__ == '__main__':

    EpisodeLoader().load()
    # print(storage.engine.execute("SELECT * FROM episodes").fetchall())
