import logging
import tweepy
import artist as art
import api as apt
import time
import shutil
import os

auth = tweepy.OAuthHandler(apt.CONSUMER_KEY, apt.CONSUMER_SECRET_KEY)
auth.set_access_token(apt.ACCESS_TOKEN, apt.ACCESS_TOKEN_SECRET)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_id_replied(m_id):
    with open('mentdb.txt', "r") as f:
        mentid = m_id
        for id in f:
            if mentid == int(id):
                return True

    f = open('mentdb.txt', 'a')
    f.write("\n" + str(m_id))
    f.close()

    return False

def check_mentions(api, keywords, since_id):
    logger.info("loading ments")
    new_since_id = since_id
    for mention in api.mentions_timeline(since_id=since_id):
        new_since_id = max(mention.id, new_since_id)

        get_ment_expanded = api.get_status(mention.id, tweet_mode='extended', include_ext_alt_text=True)._json['entities']['urls']

        if any(keyword in mention.text.lower() for keyword in keywords) or (len(get_ment_expanded)==1 and keywords[1] in get_ment_expanded[0]['expanded_url']):
            flag = check_id_replied(mention.id)
            if flag:                                #mention already replied
                continue
            if len(get_ment_expanded) == 0:
                user_id = mention.text.split()[-1][13:]
            else:
                user_id = get_ment_expanded[0]['expanded_url'][30:]
                user_id = user_id.split("?")[0]

            print(mention.text, " - ", mention.id)
            print(user_id)
            logger.info(f"FOUND USER_ID: {user_id}")
            logger.info(f"Answering to {mention.user.name}")
            status = art.get_most_artists(user_id)
            if len(status)< 70:
                logger.info(f"COULDNT FIND RESULT/PLAYLIST")
            img = os.path.normpath(os.getcwd() + "\\photos/result.jpg")
            api.update_with_media(img,status=status, in_reply_to_status_id=mention.id, auto_populate_reply_metadata=True) #reply
            shutil.rmtree("C:/Users/servet/Desktop/twitter-spotifypl/photos")
            time.sleep(15)
    return new_since_id


def main():
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    since_id = 1
    while True:
        since_id = check_mentions(api, ["spotify:user:","https://open.spotify.com/user"], since_id)
        logger.info("waitin")
        time.sleep(10)


if __name__ == "__main__":
    main()
