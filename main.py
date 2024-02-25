import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import openai
import asyncio
import logging
import re

# Load environment variables from .env file
load_dotenv()

# Discord Bot Token
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# OpenAI API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Parse the list of channel IDs from the environment variable and convert it to a set
CHANNEL_IDS = os.getenv('CHANNEL_IDS')
if CHANNEL_IDS:
    CHANNEL_IDS = set(map(int, CHANNEL_IDS.split(',')))
else:
    CHANNEL_IDS = None

# Starting message for image analysis
STARTING_MESSAGE = os.getenv('STARTING_MESSAGE', "What’s in this image? If the image is mostly text, please provide the full text.")

# Max tokens amount for OpenAI ChatCompletion
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 300))

# Message prefix
MESSAGE_PREFIX = os.getenv('MESSAGE_PREFIX', "Image Description:")

# Flag to determine if the bot should reply to image links
REPLY_TO_LINKS = os.getenv('REPLY_TO_LINKS', 'true').lower() == 'true'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Discord bot with intents for messages and message content
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Ensure the OpenAI API key is set
openai.api_key = OPENAI_API_KEY

async def describe_image(image_url):
    try:
        logger.info("Sending request to OpenAI for image analysis...")
        
        # Send a chat completion request to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": STARTING_MESSAGE},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                    ],
                }
            ],
            max_tokens=MAX_TOKENS,
        )

        logger.info("Received response from OpenAI.")

        # Extracting and returning the response
        if response.choices and len(response.choices) > 0:
            full_description = response.choices[0].message['content']
            
            # Split the description into chunks of max_message_length
            max_message_length = 1800  # Discord message character limit
            description_chunks = [full_description[i:i+max_message_length] for i in range(0, len(full_description), max_message_length)]
            
            return description_chunks
        else:
            return ["Failed to obtain a description from OpenAI."]

    except Exception as e:
        logger.error(f"Error analyzing image with OpenAI: {e}")
        return ["Error analyzing image with OpenAI."]

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    # Ignore messages sent by the bot
    if message.author == bot.user:
        return

    # Check if no specific channels are specified or if the message is in one of the specified channels
    if not CHANNEL_IDS or message.channel.id in CHANNEL_IDS:
        # Process attachments if any
        if message.attachments:
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(ext) for ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']):
                    description_chunks = await describe_image(attachment.url)

                    original_message = None  # Store the original message containing the image attachment
                    
                    # Send each description chunk as a separate message
                    for i, chunk in enumerate(description_chunks):
                        # Split message into multiple parts if exceeds the character limit
                        while chunk:
                            # Truncate the chunk to fit within the Discord message length limit
                            truncated_chunk = chunk[:1800]
                            # Send the message as a reply to the original message
                            if i == 0:
                                original_message = await message.reply(f"{MESSAGE_PREFIX} {truncated_chunk}")
                                logger.info("Sending message to Discord...")
                                logger.info("Message sent successfully.")
                            else:
                                # Send subsequent messages as replies to the original message
                                await original_message.reply(truncated_chunk)
                                logger.info("Sending message to Discord...")
                                logger.info("Message sent successfully.")
                            # Wait for a short delay before sending the next message to avoid rate-limiting
                            await asyncio.sleep(1)
                            chunk = chunk[1800:]

        # Process image links if enabled
        if REPLY_TO_LINKS:
            # Extract URLs from the message content
            message_content = message.content.lower()  # Convert message content to lowercase for case-insensitive matching
            urls = re.findall(r'(https?://[^\s]+)', message_content)

            # Filter out URLs ending with supported image file extensions
            image_urls = [url for url in urls if url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]

            # Process each image URL
            for image_url in image_urls:
                description_chunks = await describe_image(image_url)

                original_message = None  # Store the original message containing the image attachment
                
                # Send each description chunk as a separate message
                for i, chunk in enumerate(description_chunks):
                    # Split message into multiple parts if exceeds the character limit
                    while chunk:
                        # Truncate the chunk to fit within the Discord message length limit
                        truncated_chunk = chunk[:1800]
                        # Send the message as a reply to the original message
                        if i == 0:
                            original_message = await message.reply(f"{MESSAGE_PREFIX} {truncated_chunk}")
                            logger.info("Sending message to Discord...")
                            logger.info("Message sent successfully.")
                        else:
                            # Send subsequent messages as replies to the original message
                            await original_message.reply(truncated_chunk)
                            logger.info("Sending message to Discord...")
                            logger.info("Message sent successfully.")
                        # Wait for a short delay before sending the next message to avoid rate-limiting
                        await asyncio.sleep(1)
                        chunk = chunk[1800:]

# Run the bot
bot.run(DISCORD_BOT_TOKEN)
