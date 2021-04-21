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

        if any(keyword in mention.text.lower() for keyword in keywords):
            flag = check_id_replied(mention.id)
            print(mention.text, " - ", mention.id)
            if flag:                                #mention already replied
                continue
            user_id = mention.text.split()[-1][13:]
            logger.info(f"FOUND USER_ID: {user_id}")
            logger.info(f"Answering to {mention.user.name}")
            status = art.get_most_artists(user_id)
            #if len(len(status)< 70):
            #    logger.info(f"COULDNT FIND RESULT/PLAYLIST")
            img = os.path.normpath(os.getcwd() + "\\photos/result.jpg")
            api.update_with_media(img,status=status, in_reply_to_status_id=mention.id, auto_populate_reply_metadata=True) #reply
            shutil.rmtree("C:/Users/servet/Desktop/twitter-spotify/photos")
            time.sleep(100)
    return new_since_id


def main():
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    since_id = 1
    while True:
        since_id = check_mentions(api, ["spotify:user:"], since_id)
        logger.info("waitin")
        time.sleep(10)


if __name__ == "__main__":
    main()
