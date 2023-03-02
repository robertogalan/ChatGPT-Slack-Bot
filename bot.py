SLACK_BOT_TOKEN = "xoxb-0000000000000000000000000000"
SLACK_APP_TOKEN = "xapp-0000000000000000000000000000000000000000000000000000000000000000000"
OPENAI_API_KEY  = "sk-000000000000000000000000000"

import os
import openai
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_bolt import App

# Set up the Slack bot and Socket Mode handler
app = App(token=SLACK_BOT_TOKEN) 

# Set up the Slack Web API client
client = WebClient(SLACK_BOT_TOKEN)

# Define a listener function for message events
@app.event("message")
def handle_message_events(event, logger):
    if "text" in event:
        # Extract the text of the user's message
        message_text = event["text"]

        # Create a prompt for OpenAI
        prompt = "Reply to this message: " + message_text

        # Call the OpenAI API
        openai.api_key = OPENAI_API_KEY
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        ).choices[0].text.strip()

        # Post the OpenAI response to the same channel as the original message
        client.chat_postMessage(channel=event["channel"], text=response)

# Set up the Socket Mode handler
handler = SocketModeHandler(app_token=SLACK_APP_TOKEN, app=app)

# Start the Socket Mode handler
if __name__ == "__main__":
    handler.start()
