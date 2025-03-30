# Deepgram - Instagram Bot with Deepseek Chat API

This project automates the process of reading Instagram DMs and generating human-like responses using the Deepseek Chat API. It is also a post scheduler for pre-made content. 
## Features

- **Instagram DM Processing:**  
  Reads unread DMs from both the regular and pending inbox.
  
- **Deepseek Chat Integration:**  
  Uses Deepseek Chat API to generate human-like responses based on incoming DM content.
  
- **Photo Posting:**  
  Uploads photos with captions to Instagram.

- **Photo Posting:**  
  Uploads stories to Instagram.
  
- **Logging & Error Handling:**  
  Detailed logging and try/except blocks to help diagnose issues and improve robustness.
  
- **Environment-based Configuration:**  
  Sensitive information like API keys and login credentials are loaded from environment variables.

## Project Structure

- **automate_page.py:**  
  Main entry point for the project. Handles Instagram login, sets delays to mimic human behavior, and triggers DM processing.

- **message_handler.py:**  
  Contains functions for saving, loading, and processing DM threads. It also calls the Deepseek API module to generate responses.

- **deepseek_api.py:**  
  Integrates with the Deepseek Chat API to generate responses for incoming messages. Includes logic to ignore trivial messages. Sends responses to other parties.

- **posting.py:**  
  A content management system that handles Instagram post/story scheduling, prevents duplicate posts/stories, and manages image uploads with captions

## Prerequisites

- **Python 3.8+**  
- **Dependencies:**  
  Install the required packages using:
  ```bash
  pip install -r requirements.txt

### Environment Variables

Create a .env file in the root directory of the project to store sensitive information. For example:
```
USERNAME=your_instagram_username
PASSWORD=your_instagram_password
DEEPSEEK_API_KEYS=your_deepseek_api_key
```
## Roadmap and Future Features

- **Flagging Important Messages:**  
  A function to mark important messages so that they are not missed by being auto-replied to.

- **Fectch Content From Email:**  
  A system for getting, organising, and publishing content. This will allow account owners to simply email the type of content they want published and at what time. This is convenient for business owners using Instagram as a marketing tool.



