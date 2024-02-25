# Vistell: A Discord Bot for the OpenAI GPT-4 Vision API

![Vistel Logo](https://cdn.bad.download/vistell/vistell-logo-github.png)

## Overview

Vistell is a Discord bot that can describe the images posted in your Discord server using the OpenAI GPT Vision API (`gpt-4-vision-preview`).

> [!IMPORTANT]
> **This is a proof-of-concept and is not actively maintained.** No ongoing support is provided, and no updates are planned.

To use this bot:

* You'll need to host the bot yourself, on a platform that supports Docker.
* You'll need to bring your own OpenAI API Key, and pay OpenAI for your usage ([pricing](https://openai.com/pricing)).
* You'll be on your own if things break or behave unexpectedly.

Don't use this bot for production services without the expertise to maintain, troubleshoot, and improve it yourself.

## Features

The bot provides basic functionality out of the box.

* The bot will monitor for uploaded images, including when multiple images are uploaded to a single message.
* The bot can optionally monitor for URLs/linked images within text posts, including posts that contain multiple links.
     * Note: The URLs/links must end with a supported file type. Gifs sent via the Discord search tool are unsupported, see limitations below.
* When responding, the bot will use the reply system for easy navigation and notification.
* If the response exceeds the Discord message length limit, the response will be split into multiple messages.

## Customization

The bot supports some basic customization via the `.env` file.

_Note: The Discord developer portal allows you to customize the name and display photo of your bot._

* Choose which channels the bot responds in, or allow it to respond everywhere.
* Choose your max token usage per request to optimize for cost and speed.
* Choose whether the bot responds to just image attachments or also to URLs/linked images in text messages (like inserted gifs).
* Choose the starting message for the bot to set a personality.
     * Examples: Tell the bot to keep replies short, or to provide great detail. Tell the bot to use a lot of British slang when responding.
* Choose a custom message prefix displayed when responding.
     * Examples: "Image Description:", or "👁️".


## Known Limitations

There are some known limitations of the bot. There are no plans to fix these (but feel free to do so yourself!).

* URL/links to Tenor or Giphy gifs are not supported. This includes gifs sent via the Discord gif search tool. These sites serve the gifs from full webpages, and the OpenAI API doesn't know how to handle that.
* Spoilers are not respected. If an uploaded image or URL/link is marked as a spoiler, the bot will still process the image and provide a description, possibly spoiling something. It doesn't appear that the Discord API allows applications to see the spoiler status of uploaded images, so this isn't possible. It may be possible to detect for URL/links, but that isn't currently implemented.
* Limited Filetype Support. The OpenAI API currently supports PNG (.png), JPEG (.jpeg and .jpg), WEBP (.webp), and non-animated GIF (.gif).
* Limited Upload Size. The OpenAI API restricts uploaded image size to 20MB per image.
* Uses an out of date OpenAI Library. The bot uses version 0.28 of the [OpenAI python library](https://pypi.org/project/openai/), which is out of date.

## Setup

### Step 1) Prepare your Environment

1) [Install Docker](https://www.docker.com/), a tool for running containers.
2) Download the bot's files to your computer:
     * Open a terminal / command prompt and run:
     * `git clone https://github.com/BadDownload/vistell-discord-bot-with-gpt-vision.git`
3) In the downloaded files, rename `example.env` to `.env`.
     * You may need to enable displaying hidden files in your operating system to see the file.

### Step 2) Create a Discord Bot

Someone else has already written good instructions for this. [Go see their steps, which have screenshots.](https://github.com/Zero6992/chatGPT-discord-bot#step-1-create-a-discord-bot)

Once you have your Discord Token, paste it into your `.env` file in the `DISCORD_BOT_TOKEN=` section.

Tip: Be sure you following all the steps and have invited your bot into your Discord server.

### Step 3) Create an OpenAI API Key

Note: These steps could change. Check the OpenAI quick start guide for the latest instructions.

1) [Create an OpenAI account.](https://platform.openai.com/signup)
2) [Navigate to your account's API Keys page.](https://platform.openai.com/account/api-keys)
3) Click "Create new secret key".
     * This key is important and should be kept secret and secure.

Once you have your API Key, paste it into your `.env` file in the `OPENAI_API_KEY=` section.

Suggestion: Spend a few minutes to review and understand the OpenAI billing tools, including the option to set spending limits.

### Step 4) Configure the Bot

Review your `.env` file and choose your settings. If you change your mind later, that's okay. You can simply delete your container and volume, change your `.env` file settings, and rebuild the bot.

* `DISCORD_BOT_TOKEN=` Paste your Discord token from the above step here.
* `OPENAI_API_KEY=` Paste your OpenAI API key from the above step here.
* `CHANNEL_IDS=` Specify which Channel IDs the bot should respond to, in a comma separated list.
     * Leaving this blank will result in the bot responding in all channels.
     * Obtaining your Channel ID is easy but requires enabling developer mode in settings. There are good guides for this on the web.
* `STARTING_MESSAGE=` Specify what the starting message/prompt should be for your bot. Use this to set a personality.
* `MAX_TOKENS=` Specify the max amount of tokens per request. Lower is cheaper and faster, but setting too low may result in responses seeming to be "cut off".
* `MESSAGE_PREFIX=` Specify the prefix that will appear in front of responses posted by the bot.
* `REPLY_TO_LINKS=` Specify if the bot should also respond to URLs/links to images. `true` responds to everything, `false` responds only to uploaded images.

### Step 5) Create and Run the Bot

1) Open terminal / command prompt and navigate to the folder containing the downloaded files.
2) Run `docker build -t vistell-discord-bot .`
3) Wait for the container to build.
4) Run `docker run --env-file .env --name vistell-discord-bot vistell-discord-bot`
5) Upload an image and give it a test!

## Frequently Asked Questions

### Why name this "Vistell"?

It's a vision bot that can tell you things, so I named it Vistell.

### Why did you build this bot?

I wanted a Discord bot that leveraged OpenAI's Vision API. I didn't find any existing bots that supported that functionality. I was also curious if ChatGPT could write the code for such a bot. This was a fun project that provided an excuse to have ChatGPT write code, with a specific use-case for the code in mind.

### What are the use-cases of a bot like this?

* It's kinda neat, and very impressive to folks who aren't aware of how far computer vision has come.
* It essentially generates alt-text, which can help make things more accessible.
* If you really want, it could be used for OCR-like workflows.

### Shouldn't this be a feature of a bot, and not a bot itself?

Yeah. Probably.

## Legal

### CODE LICENSE

Public Domain / No Rights Reserved. The majority of this code was generated by ChatGPT and may not be eligible for copyright protection in many countries. I make no claims of copyright ownership over any parts of the code that were human written. My intention is for this code to be freely available and in the public domain.

### LOGO

(c) 2024 Bad Download.

### WARRANTY

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
