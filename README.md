# ADDReC: Anonymized Disability Discourse Reddit Corpus  [أدرك](https://www.almaany.com/en/dict/ar-en/%D8%A3%D8%AF%D8%B1%D9%83/#:~:text=%D8%A3%D8%AF%D8%B1%D9%83%20%2D%20Translation%20and%20Meaning%20in%20Almaany%20English%20Arabic%20Dictionary&text=%2D%20Come%20to%20know%20about%20%2D%20learn,find%20out%3B%20apprehe...)

## Citation
Paper: [Large-Scale Anonymized Text-based Disability Discourse Dataset](https://dl.acm.org/doi/10.1145/3597638.3614476) 

## Data

Reddit comments from three subreddits over a 5 year period (January 2015- Decemeber 2019).
Subreddits:

- r/Blind
- r/Disability
- r/ADHD

### Sensitive data anonymized

- names
- usernames of the form `\u\username`
- locations
  - zip codes
  - public named locations
- links to external sites

### Attributes of each entry

| Attribute        | Description                                                                                                                                                       |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| commentator_id   | Unique id of username of poster                                                                                                                                   |
| created_utc      | Timestamp (in UTC) of post                                                                                                                                        |
| anonymized_body  | Body of comment that has been passed through presidio anonymizer                                                                                                  |
| anonymized_masks | indicates what data was masked out from the original comment body. This information is sensitive and should not be included in any data made publically available |
| ups              | community up votes                                                                                                                                                |
| downs            | community down votes                                                                                                                                              |
| score            | ups - downs                                                                                                                                                       |
| controversiality | a score based on ratio of up votes to down votes                                                                                                                  |
| gilded           | a reward given by users to other users for a good post, bought with real money                                                                                    |
| distinguished    | official statement by a moderator                                                                                                                                 |

## Presidio Anonymization

Identifiers to be masked by the presidio anonymization system.

### Global identifiers

- CREDIT_CARD
- CRYPTO
- EMAIL_ADDRESS
- IBAN_CODE
- IP_ADDRESS
- LOCATION
- PHONE_NUMBER
- PERSON
- PHONE_NUMBER
- URL

### United states

- US_BANK_NUMBER
- US_DRIVER_LICENSE
- US_ITIN
- US_PASSPORT
- US_SSN

### Uk

- UK_NHS

### Spain

- NIF

### Singapore

- FIN

### Australia

- AU_ABN
- AU_ACN
- AU_TFN
- AU_MEDICARE

### Custom

- USER
  - this one was manually defined to catch `/u/username`
  - regex string: `r'/u/([a-zA-Z0-9_]*)\b'`
  - everytime a username is identified, an additional regex is made just for that portion.

## Important Functions

### `reddit_anonymizer.py`

#### `anonymize_dataframe(csv_df: pd.DataFrame) -> pd.DataFrame`

Anonymize a single dataframe. Each DataFrame is a single month of a subreddit.

1. scrape file for usernames to add to registry
2. load original registry and masks
3. mask every comment and store any results in next col over

#### `anonymize_text(sentence: str, analyzer) -> str:`

Run the anonymization process on every dataframe.

### `reddit_dataset.py`

#### `load_dataset() -> Dict[str, Dict[int, Dict[int, pd.DataFrame]]]:`

load all csvs from reddit data set into dataframes.

##### structure

- subreddit: dict[subreddit, dict]
  - year: dict[year, dict]
    - month: dict[month, dataframe]

#### `print_dataset(data: Dict[str, dict]) -> None:`

print out the whole loaded dataset

## Notes:

### Current State

We used the [presidio anonymizer](https://microsoft.github.io/presidio/anonymizer/), but found issues with its name recognition system.
It worked very well for identifying raw number ID's, but the named entity recognition tends to miss named locations and grab onto medication names.

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)](LICENSE).
