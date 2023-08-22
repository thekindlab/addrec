import pandas as pd

from typing import Dict
from constants import SUBREDDITS, YEARS, MONTHS, DATA_PATH
from pathlib import Path



class RedditDataset:
    def __init__(self, data_path='anonymized_first_pass/'):
        self.data_path = data_path
        self.data = self.load()
    
    def load(self) -> Dict[str, Dict[int, Dict[int, pd.DataFrame]]]:
        '''Load all CSVs from the dataset into DataFrames.'''
        '''
        load all csvs from reddit data set into dataframes
        - subreddit: dict[subreddit, dict]
            - year: dict[year, dict]
                -month: dict[month, dataframe]
        '''
        print("**** LOADING DATASET ****")
        subreddit_dictionaries: dict = dict.fromkeys(SUBREDDITS)
        # for each subreddit
        for sr in SUBREDDITS:
            print("importing /r/"+sr+"...")
            year_dictionary: dict = dict.fromkeys(YEARS)
            # process each subreddits years
            for year in YEARS:
                print(year)
                month_dictionary: dict = dict.fromkeys(MONTHS)
                for fp, month in zip(sorted(Path(self.data_path+sr+str(year)).rglob('*.csv')), MONTHS):
                    print(fp, month)
                    with open(fp) as fd:
                        df = pd.read_csv(fd)
                        month_dictionary[month] = df
                year_dictionary[year] = month_dictionary
            subreddit_dictionaries[sr] = year_dictionary
        return subreddit_dictionaries
    
    def print(self) -> None:
        '''Print out the loaded dataset.'''
      
        print("**** PRINTING DATASET ****")
        for sr, year_dict in self.data.items():
            print(sr)
            for year, month_dict in year_dict.items():
                print(year)
                for month, df in month_dict.items():
                    print(month)