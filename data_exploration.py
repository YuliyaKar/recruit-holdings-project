"""
  Recruit Holdings Kaggle Competition.

  Inspired by the following Kaggle kernels:
    -
    -
    -

  author: YuliyaK
  date: 2/2/2018
"""

import pandas as pd
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
