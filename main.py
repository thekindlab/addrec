from reddit_anonymizer import RedditAnonymizer
from reddit_dataset import RedditDataset
from username_recognizer import UsernameRecognizer


columns_to_drop  = [
                'score_hidden',
                'archived', 
                'name',
                'author',
                'author_flair_text',
                # 'created_utc',
                'subreddit_id',
                'link_id',
                'parent_id',
                'retrieved_on',
                'id',
                'subreddit',
                'author_flair_css_class',
                'anonymized_masks.1',
                'anonymized_body.1',
                'anonymized_masks'
                ]

def main():
    dataset = RedditDataset(data_path='anonymized_first_pass/')
    anonymizer = RedditAnonymizer()
    for sr, year_dict in dataset.data.items():
        for month, month_dict in year_dict.items():
            for year, df in month_dict.items():
                df = anonymizer.anonymize_dataframe(df)
                df.drop(columns_to_drop, axis=1, inplace=True)
                df.rename(columns={'user_id': 'commentator_id'}, inplace=True)

                df = df[['commentator_id', 'created_utc', 'anonymized_body', 'anonymized_masks', 
                     'ups', 'downs', 'score', 'controversiality', 'gilded', 'distinguished']]
                #TODO = Make directory for subreddit and year if it does not exist and add to file path
                df.to_csv('./test/anonymized-'+sr[:-1].lower()+'-'+str(month)+str(year)+'.csv')
                break

    username_recognizer = UsernameRecognizer()
    results = username_recognizer.find_usernames(dataset.data)
    username_recognizer.save_matches(results)

if __name__ == "__main__":
    main()
