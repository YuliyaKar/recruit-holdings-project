"""
  Recruit Holdings Kaggle Competition.

  Inspired by the following Kaggle kernels:
    - the1owl https://www.kaggle.com/the1owl/surprise-me
    - festa78 https://www.kaggle.com/festa78/simple-xgboost-lb-0-495
    - DSEverything https://www.kaggle.com/dongxu027/mean-mix-math-geo-harmonic-lb-0-493

  author: YuliyaK
  date: 2/2/2018
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_data():
    data = {'air_reserve': pd.read_csv('data/air_reserve.csv'),
            'air_store_info': pd.read_csv('data/air_store_info.csv'),
            'air_visit_data': pd.read_csv('data/air_visit_data.csv'),
            'date_info': pd.read_csv('data/date_info.csv'),
            'hpg_reserve': pd.read_csv('data/hpg_reserve.csv'),
            'hpg_store_info': pd.read_csv('data/hpg_store_info.csv'),
            'store_id_relation': pd.read_csv('data/store_id_relation.csv'),
            'test': pd.read_csv('data/sample_submission.csv'),
            }

    return data

def prepare_data(data):

    #Join select restaurants from hpg system that are in air system.
    data['hpg_reserve'] = pd.merge(data['hpg_reserve'], data['store_id_relation'],
                                    how='inner', on=['hpg_store_id'])

    #Change dates to datetime dtype + round it to date only.
    for df in ['hpg_reserve', 'air_reserve']:
        data[df]['visit_datetime'] = pd.to_datetime(data[df]['visit_datetime'])
        data[df]['visit_datetime'] = data[df]['visit_datetime'].dt.date
        data[df]['reserve_datetime'] = pd.to_datetime(data[df]['reserve_datetime'])
        data[df]['reserve_datetime'] = data[df]['reserve_datetime'].dt.date

def add_reserve_date_diff(data):
    #Create new feature for time difference between reservation
    # and actual visit
    for df in ['hpg_reserve', 'air_reserve']:
        data[df]['reserve_datetime_diff'] = data[df].apply(
            lambda r: (r['visit_datetime'] - r['reserve_datetime']).days,axis=1)

def group_reservation_data(data):
    """ Group by store ID and visit date"""

    #Sum reserve_datetime_diff - I don't really agree with it...
    for df in ['hpg_reserve', 'air_reserve']:
        data[df] = data[df].groupby(['air_store_id', 'visit_datetime'],
                    as_index=False)[['reserve_datetime_diff', 'reserve_visitors']].sum().rename(columns=
                    {'visit_datetime':'visit_date'})

def handle_dates(data, df):
    """ Add separate date columns """

    data[df]['visit_date'] = pd.to_datetime(data[df]['visit_date'])
    data[df]['dow'] = data[df]['visit_date'].dt.dayofweek
    data[df]['year'] = data[df]['visit_date'].dt.year
    data[df]['month'] = data[df]['visit_date'].dt.month
    data[df]['visit_date'] = data[df]['visit_date'].dt.date

    return data

def prepare_visit_data(data):
    """ Change datetime type and add new features """

    df = 'air_visit_data'
    data = handle_dates(data, df)

def prepare_test_data(data):
    """ Make the same changes to submission test data. """
    df = 'test'

    # Split id to air_store_id and visit_time
    data[df]['visit_date'] = data[df]['id'].map(lambda x: str(x).split('_')[2])
    data[df]['air_store_id'] = data[df]['id'].map(lambda x: '_'.join(str(x).split('_')[:2]))

    data = handle_dates(data, 'test')

def create_stores_df(data):
    """ Create a DataFrame containing 2 columns: 1 column fot store IDs from
        test data, and 1 column encoding day of week (from 0 to 6). Each unique
        store ID has 7 entry rows corresponsing to 7 days of week.
    """
    unique_stores = data['test']['air_store_id'].unique()
    stores = pd.concat([pd.DataFrame({'air_store_id': unique_stores, 'dow':
                        [i]*len(unique_stores)}) for i in range(7)], axis=0,
                        ignore_index=True).reset_index(drop=True)

    return stores
