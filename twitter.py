from config import Config
from requests_oauthlib import OAuth1, OAuth1Session
import requests
import pprint
from urllib import parse

config = Config()

def generate_oauth_token():
    token = OAuth1(
    config.TWITTER_CONSUMER_KEY,
    config.TWITTER_CONSUMER_SECRET_KEY,
    config.TWITTER_ACCESS_TOKEN,
    config.TWITTER_ACCESS_TOKEN_SECRET)

    return token

def generate_tweets(search, analysts=config.ANALYSTS):

    token = generate_oauth_token()

    ## build URL here

    url = config.TWITTER_SEARCH_BASE_URL + '?q='

    from_accounts = 'from:'

    for i, account in enumerate(analysts.values()):
        if i == 0:
            from_accounts = from_accounts + account
        else:
            from_accounts = from_accounts + ' OR ' + account

    search_values = ''
    for i, val in enumerate(search):
        if i == 0:
            search_values = search_values + val
        else:
            search_values = search_values + ' OR ' + val

    first_query = parse.quote(from_accounts + search_values)

    url = url + first_query

    SEARCH_PARAMS = {
        'count': '100',
        'lang': 'en',
        'include_entities': False
    }

    res = requests.get(
        url,
        params=SEARCH_PARAMS,
        auth=token
    )

    tweets = res.json().get('statuses')

    parsed_tweets = []

    for tweet in tweets:
        truncated = tweet.get('truncated')
        text = tweet.get('text')

        if truncated or 'RT' in text:
            continue

        for q in search:
            if q in text:
                parsed_tweets.append(text)

    return parsed_tweets

if __name__ == '__main__': # this file is not being imported
    pprint.pprint(
        generate_tweets(['Aaron Jones', 'A. Jones']) # test our code here
    )
