from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from openai import OpenAI
import os 
import json
import logging

load_dotenv() # For script to access env file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', 
                    handlers=[logging.FileHandler("bot_activity.log"),
                            logging.StreamHandler()])
logger = logging.getLogger()

API_KEYS = os.getenv("DEEPSEEK_API_KEYS")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
API_URL = "https://api.deepseek.com"


system_prompt = (SYSTEM_PROMPT)

def respond_to_other_party(response, other_party_id, user):

  """
  Sends the Deepseek DM  to the other party.
  """
  try:
        user.direct_send(response, other_party_id)
        logger.info(f"Sent DM to other_party_id:{other_party_id}. Response: {response}\n")
  except Exception as e:
      logger.info(f"Unable to send DM ( {response}) back to user( {other_party_id}). Error{e}" )

def POST_deepseek(regular_text):

    """
    Requests a DM messages from the Deepseek API to generate a human like response.
    """
    try:
        client = OpenAI(api_key=f"{API_KEYS}", base_url=f"{API_URL}")

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": regular_text },
            ],
            stream=False
        )

        deepseek_response = response.choices[0].message.content

        return deepseek_response

    except Exception as e:
        logger.info("Unable to fetch Deepseek's response %s" % e)

def process_text(new_messages, user):

    """
    Handles processing the text to make sure no trivial messages are sent. 
    Also, makes sure that regular and pending DMs are separated 
    """
    try:
        text = new_messages.values() 
        latest_DM = [next(iter(item.values())) for item in text]
        
        if latest_DM:
            if len(latest_DM[0]) > 2:
                regular_text = latest_DM[0]
                
                AI_response = POST_deepseek(regular_text)    
                sender_id = [ 
                    list(inner_dict.keys())[0]
                    for thread_id, inner_dict in new_messages.items()
                    if list(inner_dict.values())[0] == regular_text
                ]
               
                respond_to_other_party(AI_response, sender_id, user)

            if len(latest_DM) >= 2 and len(latest_DM[1]) > 2:
                    pending_text = latest_DM[1]
                 
                    AI_response_pending = POST_deepseek(pending_text)    
                    sender_id_pending = [ 
                        list(inner_dict.keys())[0]
                        for thread_id, inner_dict in new_messages.items()
                        if list(inner_dict.values())[0] == pending_text
                    ]

                    respond_to_other_party(AI_response_pending, sender_id_pending, user)

            else:
                pass
        else:
            print(f"Maybe there are no new messages: {new_messages}")
                  
    except Exception as e:
        logger.info("Couldn't isolate text: %s" % e)

    