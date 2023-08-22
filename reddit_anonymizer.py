import pandas as pd
import uuid 
import re

from tqdm import tqdm

from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer, RecognizerRegistry
from presidio_anonymizer import AnonymizerEngine

from typing import List, Tuple

class RedditAnonymizer:
    '''Initialize the RedditAnonymizer with default values.'''

    def __init__(self):
        self.username_to_id = {}
        self.masks = [
               # global identifiers
            'CREDIT_CARD',
            'CRYPTO',
            'EMAIL_ADDRESS',
            'IBAN_CODE',
            'IP_ADDRESS',
            'LOCATION',
            'PHONE_NUMBER',
            'PERSON',
            'PHONE_NUMBER',
            'URL',
            # united states
            'US_BANK_NUMBER',
            'US_DRIVER_LICENSE',
            'US_ITIN',
            'US_PASSPORT',
            'US_SSN',
            # uk
            'UK_NHS',
            # spain
            'NIF',
            # singapore
            'FIN',
            # australia
            'AU_ABN',
            'AU_ACN',
            'AU_TFN',
            'AU_MEDICARE',
            # custom
            'USER'
        ]
        self.user_recognizer = self._create_user_recognizer()
    
    def _create_user_recognizer(self) -> PatternRecognizer:
        '''Create default user recognizer for Reddit.
        
        This is a pattern recognizer for /u/User.
        '''
        regex_search = Pattern(
            name='reddit_user',
            regex=r'/u/([a-zA-Z0-9_]*)\b',
            score=1
        )

        return PatternRecognizer(
            supported_entity='USER',
            patterns=[regex_search]
        )
    
    def anonymize_text(self, sentence: str, analyzer) -> Tuple:
        '''Anonymize a text and return the anonymized result and anonymization info.'''

        # Call analyzer to get results
        results = analyzer.analyze(
            text=sentence,
            entities=self.masks,  # use all entities defined in global mask list
            language='en'
        )
        # Analyzer results are passed to the AnonymizerEngine for anonymization
        anonymizer = AnonymizerEngine()
        anonymized_text = anonymizer.anonymize(
            text=sentence,
            analyzer_results=results
        )

        return results, anonymized_text

    def generate_username_pattern(self, name: str, user_registry) -> None:
        '''Generate and add a username recognizer pattern to the registry.'''

        
        '''take username and create a case insensitive pattern'''
        print("generating regex for", name, " (?i)\\b"+name+"\\b")
        uname_pattern = Pattern(
            name='generated'+name,
            regex=r'(?i)\b'+name+r"\b",
            score=0.5
        )
        entity_name = 'REDDIT_NAME'
        uname_recognizer = PatternRecognizer(
            supported_entity=entity_name,
            patterns=[uname_pattern]
        )
        self.masks.append(entity_name)
        # load new recognizer into recognizer registry
        user_registry.add_recognizer(uname_recognizer)
    

    def check_username(self, results, text, reddit_usernames, user_registry) -> List[str]:
        '''Check results for new usernames and add them to the registry.'''

        # results is list of (.type, .start, .end, and .score)
        # ann
        for match in results:
            match = match.to_dict()
            if match['entity_type'] == 'USER':
                user_name = text[match['start']+3:match['end']]
                if user_name not in reddit_usernames:
                    # make a regex for just this name
                    self.generate_username_pattern(user_name, user_registry)
                    reddit_usernames.append(user_name)
        return reddit_usernames
    
    def anonymize_dataframe(self, csv_df: pd.DataFrame) -> pd.DataFrame:
        '''
        now that we've added all usernames to recognizers,
        lets load the default ones and anonymize all data.
        we will store any results in a new col (or None)
        '''
    #      1. scrape file for usernames to add to registry
    #      2. load original registry and masks
    #      3. mask every comment and store any results in next col over

        # keep track of each new regex so we dont double up
        reddit_usernames: List[str] = []
        # reset registry
        user_registry = RecognizerRegistry()
        # registry.load_predefined_recognizers()
        user_registry.add_recognizer(self.user_recognizer)
        # load spaCy model
        analyzer = AnalyzerEngine(registry=user_registry)

        print(csv_df)

        csv_df['user_id'] = csv_df['author'].apply(self._get_or_assign_user_id)
        csv_df['body'] = csv_df.apply(lambda row: self._replace_username_with_id(row['body'], row['author']), axis=1)

        # 1. scrape each comment for usernames
        print("processing ", len(csv_df), " usernames...")
        for row, comment in tqdm(csv_df['body'].iteritems()):
            results, _ = self.anonymize_text(str(comment), analyzer)
            reddit_usernames = self.check_username(results, comment, reddit_usernames, user_registry)

        print("anonymizing ", len(csv_df), "...")
        anonymized_body: list = []
        anonymized_masks: list = []
        # 2. load all the predefined registries
        user_registry.load_predefined_recognizers()
        for row, comment in tqdm(csv_df['body'].iteritems()):
            results, anonymized = self.anonymize_text(str(comment), analyzer)
            if len(results) == 0:
                anonymized_body.append(None)
                anonymized_masks.append(None)
            else:
                anonymized_body.append(anonymized.text)
                anonymized_masks.append(anonymized.items)
        
        if anonymized_body:
            csv_df['anonymized_body'] = anonymized_body
        else:
            csv_df['anonymized_body'] = csv_df['body']
        csv_df['anonymized_masks'] = anonymized_masks
        
        return csv_df
    
    def _get_or_assign_user_id(self, author: str) -> str:
        '''Return the unique ID for an author, or assign one if it doesn't exist.'''
        if author not in self.username_to_id:
            self.username_to_id[author] = str(uuid.uuid4())
        return self.username_to_id[author]
    
    def _replace_username_with_id(self, comment: str, author: str) -> str:
        '''Replace mentions of a username in a comment with its corresponding unique ID.'''
        username_matches = re.findall(r"/u/([a-zA-Z0-9_-]+)", comment)
        for username in username_matches:
            # If the matched username is not a UUID

            if username not in self.username_to_id:
                self.username_to_id[username] = str(uuid.uuid4())
            user_id = self.username_to_id[username]
            comment = comment.replace(f"/u/{username}", f"/u/{user_id}")

        comment = comment.replace(f"/u/{author}", f"/u/{user_id}")
        return comment