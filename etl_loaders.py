from db_schema import Episode
import pandas as pd
from pandas import DataFrame
import os
from typing import Type, List


class ETLLoader:
    DATA_ROOT = os.path.join(os.getcwd(), 'data')

    print("Loading `df_colors_used`...")
    df_colors_used = pd.read_csv(os.path.join(
        DATA_ROOT, 'The Joy Of Painiting - Colors Used'))
    print("Loading `df_subject_matter`...")
    df_subject_matter = pd.read_csv(os.path.join(
        DATA_ROOT, 'The Joy Of Painiting - Subject Matter'))
    print("Loading `df_episode_dates`...")
    df_episode_dates = pd.read_csv(os.path.join(
        DATA_ROOT, 'The Joy Of Painting - Episode Dates'), delimiter="\t", header=None, columns=['input'])
    # parse data in df_episode_dates


    @classmethod
    def getCols(cls):
        for c in cls.__table__.columns:
            print(c)


class EpisodeLoader(ETLLoader, Episode):

    @classmethod
    def load(cls):
        # new df with EPISODE, TITLE from df_subjet_matter
        df = cls.df_subject_matter[["EPISODE", "TITLE"]]
        # new column - season number from EPISODE string
        df['season'] = df.apply(
            lambda r: int(r['EPISODE'].split('E')[0][1:]), axis=1)
        # new column - episode number from EPISODE string
        df['episode'] = df.apply(
            lambda r: int(r['EPISODE'].split('E')[1][1:]), axis=1)
        # update column - change TITLE to title-case & remove ""
        df['TITLE'] = df.apply(
            lambda r: str(r['TITLE']).title()[1:-1], axis=1)
        # rename columns
        df.rename(columns={"EPISODE": "id", "TITLE": "title"}, inplace=True)
        # update column order
        df = df[['id', 'season', 'episode', 'title']]


if __name__ == '__main__':

    EpisodeLoader().load()
