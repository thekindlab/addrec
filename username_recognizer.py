import re
import csv

from typing import Dict, List, Tuple

class UsernameRecognizer:
    def __init__(self):
        '''Initialize the UsernameRecognizer.'''
        self.results = []

    def find_usernames(self, data: Dict[str, dict]) -> List[Tuple[str, int, int, int]]:
        '''Find possible username matches in the dataset.'''
        # ... (rest of the global_regex function logic)
        '''
        regex every file for possible username matches
        '''
        results = []
        print("**** PRINTING DATASET ****")
        for sr, year_dict in data.items():
            print(sr)
            for year, month_dict in year_dict.items():
                print(year)
                for month, df in month_dict.items():
                    print(month)
                    for row, comment in df['body'].iteritems():
                        # force coercion due to some error entries (adhd 2017 6 4322)
                        comment = str(comment)
                        match = re.search('/u/[^\\s]', comment)
                        # if we get a match, write down (sr, year, month, row)
                        if match:
                            results.append((sr, year, month, row))
        # sort results before returning
        results = sorted(results, key=lambda x: (x[0], x[1], x[2], x[3]))
        return results

    def save_matches(self, results: List[Tuple[str, int, int, int]]) -> None:
        '''Save username matches to a CSV file.'''
        with open('matches.csv', 'w') as fd_out:
            csv_out = csv.writer(fd_out)
            csv_out.writerow(['subreddit', 'year', 'month', 'row'])
            csv_out.writerows(results)
