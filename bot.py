import os, boto3, tweepy

client = boto3.client('comprehend')



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def lambda_handler(event, context):
    trump_tweet=get_status_text()
    trump_tweet_id=get_status_id()

    sentiment=get_sentiment(trump_tweet)
    api.update_status(status=sentiment, in_reply_to_status_id=trump_tweet_id, auto_populate_reply_metadata=True)
    
    return sentiment

def get_status_text():
    return (api.get_user('@realDonaldTrump')).status.text

def get_status_id():
    return str((api.get_user('@realDonaldTrump')).status.id)

def get_sentiment(txt):
    sentiment=client.detect_sentiment(Text=txt,LanguageCode='en')
    print(sentiment)
    print(txt)
    if (sentiment['Sentiment'] == ('POSITIVE')):
        return ("He's excited. I'm scared. Positivity Score: " + str(sentiment['SentimentScore']['Positive']))
    elif (sentiment['Sentiment'] == ('NEGATIVE')):
        return ("He's pissy. Negativity Score: " + str(sentiment['SentimentScore']['Negative']))
    else:
        return "This one is pretty neutral. (Neutrality: " + str(sentiment['SentimentScore']['Neutral']) + ")"