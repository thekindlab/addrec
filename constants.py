# reddit data
DATA_PATH = './anonymized_first_pass/'
# subreddits
SUBREDDITS = ['ADHD/', 'Blind/', 'Disability/']
YEARS = range(2015, 2020)
# this is the index order months are found in (they are alphabetized)
MONTHS = [
    4,   # apr
    8,   # aug
    12,  # dec
    2,   # feb
    1,   # jan
    7,   # jul
    6,   # jun
    3,   # mar
    5,   # may
    11,  # nov
    10,  # oct
    9    # sep
]

months_alphabetized = [
    10,
    11,
    12,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9
]

ANON_PATH = './anonymized_first_pass/'
keep_attributes = [
    'anonymized_body',
    'ups',
    'downs',
    'score',
    'controversiality',
    'gilded',
    'distinguished',
    'anonymized_masks'
]