from dotenv import load_dotenv
from deepseek_api import process_text
import os 
import json
import logging

load_dotenv() # For script to access env file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                         handlers=[logging.FileHandler("bot_activity.log"),
                         logging.StreamHandler()])
logger = logging.getLogger()

def save_entire_DMs(all_threads):
    
    """
    Saves the dictionary that contains information about all threads( chats)
    """
    try:
        with open("DMs_history/entire_chats_history.json", "w") as f:
            json.dump(all_threads, f, indent=4)
    
            #print(f" Last seen messages: {all_threads} \n")
    except Exception as e:
        logger.info("Couldn't dump DM history into a JSON file: %s" % e)

def save_new_messages(last_seen_messages):

    """
    Saves the dictionary that contains the most recent message in the inbox. Both the regular and pending inbox
    """
    try:
        with open("DMs_history/last_seen_messages.json", "w") as f:
            json.dump(last_seen_messages, f, indent=4)
    
            #print(f" Last seen messages: {last_seen_messages} \n")
    except Exception as e:
        logger.info("Couldn't dump latest messages into a JSON file: %s" % e)

# Loads the data of previous DMs
def load_latest_messages():

    """
    Loads the last_seen_messages.json to compare with the current messages. if there is a difference then that message is new.
    """
    try:
        with open("DMs_history/last_seen_messages.json", "r") as f:
            content = f.read().strip()
            if not content: # if the file is empty return {}
                return {}
            latest_messages = json.loads(content)
            return latest_messages   
    
    except Exception as e:
        logger.info("Couldn't load latest messages from JSON file: %s" % e)
        return {}

def get_unread_DMs(user):

    """
    To get unread DMs and structure them in json files to be used later. 
    Also, send the latest messages to the deepseek_api script for generating a human like response.
    """
    threads_dict = {} # Store entire chat between user and other parties
    all_DMs = user.direct_threads(20)
    all_pending_DMs = user.direct_pending_inbox(20)
    old_messages = load_latest_messages()

    bot_id = user.user_id # This is your account 

    # Process regular DMs
    for thread in all_DMs:
        try:
            unread_messages = [] # Current messages for current thread( chat)

            for message in thread.messages:
                send_id = message.user_id
                text = message.text
                unread_messages.append({ send_id : text})
                threads_dict[thread.id] = unread_messages
        except Exception as e:
            logger.info("Couldn't process regular DMs: %s" % e)
    
    # Processes all Pending DMs
    for thread in all_pending_DMs:
        try:
            unread_messages = [] # Current messages for current thread( chat)

            for message in thread.messages:
                send_id = message.user_id
                text = message.text
                unread_messages.append({ send_id : text})
                threads_dict[thread.id] = unread_messages
        except Exception as e:
            logger.info("Couldn't process pending DMs: %s" % e)

    new_messages = {}

    # Gets the latest/ first message in the thread( chat) depending on where the thread is from
    try: 
        for thread_id , messages in threads_dict.items():
                if messages:
                    
                    # **If thread is NOT in `all_DMs`, it's from `all_pending_DMs`**
                    if thread_id not in [thread.id for thread in all_DMs]:
                        first_message = messages[-1]
                    else:
                        first_message = messages[0] 
                   
                    last_seen = old_messages.get(thread_id)
                    sender_id = list(first_message.keys())[0]

                    # Convert both IDs to strings for comparison
                    bot_id_str = str(bot_id)
                    sender_id_str = str(sender_id)

                    print(f"last_seen value: {last_seen}\n")
                    print(f"first message value: {first_message}\n")
                    print(f"Old messages Thread ID value: {old_messages.get(thread_id, 'No previous messages')}\n")
                    print(f"Sender ID value: {sender_id_str} (type: {type(sender_id)})\n")
                    print(f"Bot ID value: {bot_id_str} (type: {type(bot_id)})\n")
                    print(f"Is message from bot? {bot_id_str == sender_id_str}\n")
                    
                    if bot_id_str == sender_id_str:
                        # Skip messages sent by our own bot account
                        logger.info(f"Skipping message from bot's own account in thread {thread_id}")
                    else:
                        # Only process and save messages from other users
                        if last_seen != first_message:
                            new_messages[thread_id] = first_message
                            save_new_messages(new_messages)
                            print(f"New messages: {new_messages}\n")
                            logger.info(f"New message detected from user {sender_id} in thread {thread_id}")
                            # Move process_text inside this block so it only processes non-bot messages
                            process_text(new_messages, user)
                        else:
                            logger.info(f"No new message detected from user {sender_id} in thread {thread_id}")
        save_entire_DMs(threads_dict)

    except Exception as e: 
       logger.info("Couldn't find the latest messages from inbox: %s" % e)

    # Remove this line since we moved it inside the if block
    #process_text(old_messages, user) # deepseek_api.py

    #respond_to_other_party(response, other_party_id, user)


    