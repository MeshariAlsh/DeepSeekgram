from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from instagrapi.story import StoryBuilder
from instagrapi.types import StoryLink
import os 
import json
import logging
from datetime import datetime
import PIL.Image

load_dotenv() # For script to access env file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', 
                    handlers=[logging.FileHandler("bot_activity.log"),
                            logging.StreamHandler()])
logger = logging.getLogger()

def save_successful_post(post):
    try:
        with open("successful_posts.json", "w") as f:
            json.dump(post, f, indent=4)
            print(f"Successful post saved to JSON file: {post}\n")
    except Exception as e:
        logger.info(f"Couldn't save successful post to JSON file: {e}")

def load_successful_posts():
    """
    Load successful posts from JSON file.
    """
    try:
        with open("successful_posts.json", "r") as f:
            content = f.read().strip()
            if not content:  # if the file is empty return {}
                return {}
            return json.loads(content)
    except Exception as e:
        logger.info(f"Couldn't load successful posts from JSON file: {e}")
        return {}

def load_scheduled_posts():

    """
    Load scheduled posts from JSON file.
    """
    try:
        with open("scheduled_posts.json", "r") as f:
            posts = json.load(f)
            return posts
    except Exception as e:
       logger.info(f"Couldn't load post from JSON file: {e}")


def process_posts(user):

    """
    Process the posts to be uploaded to the instagram account.
    """
    try:

        previous_posts = load_successful_posts()
        scheduled_posts = load_scheduled_posts()

        for caption, image_path in scheduled_posts.items():
            if caption not in previous_posts:
                post = {caption: image_path}
                save_successful_post(post)
                print(f"Posting new post: {caption} and the image path is: {image_path}\n")
                upload_photo_post(user, caption, image_path)
    except Exception as e:
        logger.info(f"Error processing posts: {e}")

def upload_photo_post(user, caption, image_path):

    """
    Uploads an image with a predefined caption (see line 15) to the instagram account logged in (see line 11 & 12). 
    """
    try:
        media = user.photo_upload(
            path=image_path, 
            caption=caption
        )
        if media:
            logger.info("Succesfully Posted Photo.")
            print(media)
    except Exception as e:
        logger.error(f"Error posting photo: {str(e)}")

def save_successful_story(story):

    try:
        with open("successful_stories.json", "w") as f:
            json.dump(story, f, indent=4)
            print(f"Successful story saved to JSON file: {story}\n")
    except Exception as e:
        logger.info(f"Couldn't save successful story to JSON file: {e}")

def load_successful_story():
    """
    Load successful stories from JSON file.
    """
    try:
        with open("successful_stories.json", "r") as f:
            content = json.load(f)
            if not content:  
                return {}
            return content
    except Exception as e:
        logger.info(f"Couldn't load successful stories from JSON file: {e}")
        return {}

def load_scheduled_story():

    """
    Load scheduled stories from Txt file.
    """
    
    try:
        with open("scheduled_stories.json", "r") as f:
            story_path = json.load(f)
            return story_path
    except Exception as e:
        logger.info(f"Couldn't load story from TXT file: {e}")

def process_stories(user):
    """
    Process the stories to be uploaded to the instagram account.
    """
    try:
        story_path = load_scheduled_story()
        previous_stories = load_successful_story()
        today = datetime.now().strftime("%Y-%m-%d")

        if today in story_path:
            if today not in previous_stories:  # To check if the story is already posted
                story = {today: story_path[today]}
                save_successful_story(story)
                print(f"Posting new story: {today} and the image path is: {story_path[today]}\n")

                images = story_path[today]    
                for image_path in images:
                        user.delay_range = [5, 10] 
                        upload_story(user, image_path)
                        print(f"Inside Loop the image path is: {image_path}\n")
            else:
                logger.info(f"Skipping story: {today} because the scheduled date is not today")
        
        print(f"Processing {story_path} stories and the date is: {today}")
    except Exception as e:
        logger.info(f"Error processing stories: {e}")

def upload_story(user, image_path):
    """
    Uploads an image to the instagram story.
    """
    

    try:
        buildout = StoryBuilder(image_path).photo()

        user.video_upload_to_story(
            path=buildout.path
        )

        logger.info(f"Successfully Posted Story {buildout.path}.")
    except Exception as e:
        logger.error(f"Error posting story: {str(e)}")
