from message_handler import get_unread_DMs, load_latest_messages, save_new_messages
from posting import process_posts, process_stories, create_workshop_story
from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import os 
import json
import logging
import random
import time

load_dotenv() # For script to access env file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', 
                    handlers=[logging.FileHandler("bot_activity.log"),
                            logging.StreamHandler()])

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

# Update environment variable names to match .env file
IG_USERNAME = os.getenv('IG_USERNAME')
IG_PASSWORD = os.getenv('IG_PASSWORD')


def login_user(user):
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """
    login_via_session = False
    login_via_pw = False

    try:
        session = user.load_settings("session.json")

        if session:
            try:
                user.set_settings(session)
                user.login(IG_USERNAME, IG_PASSWORD)
                user.dump_settings("session.json")
                logger.info("Logged in via session")

                # check if session is valid
                try:
                    user.get_timeline_feed()
                except LoginRequired:
                    logger.info("Session is invalid, need to login via username and password")

                    old_session = user.get_settings()

                    # use the same device uuids across logins
                    user.set_settings({})
                    user.set_uuids(old_session["uuids"])

                    user.login(IG_USERNAME, IG_PASSWORD)
                login_via_session = True
            except Exception as e:
                logger.info("Couldn't login user using session information: %s" % e)

        if not login_via_session:
            try:
                logger.info("Attempting to login via username and password. username: %s" % IG_USERNAME)
                if user.login(IG_USERNAME, IG_PASSWORD):
                    user.dump_settings("session.json") # To create the session.json if first time running script
                    login_via_pw = True
            except Exception as e:
                logger.info("Couldn't login user using username and password: %s" % e)

        if not login_via_pw and not login_via_session:
            raise Exception("Couldn't login user with either password or session")
    except Exception as e:
        logger.info(f"Login via session and user info has fail {e}")
        
def main():
    user = Client() # An instance of class Client to send request to instagram# mimic human interaction
    login_user(user) 
    user.delay_range = [5, 10] 

   
    #To switch between actions and not raise instagram flags for automated behaviour
    random_float = random.random()
    if (random_float % 2 == 0 ):
         process_posts(user)
    else:
        process_stories(user)


if __name__ == "__main__":
    main()
