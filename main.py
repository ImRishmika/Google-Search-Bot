# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import os
import requests
from dotenv import load_dotenv
from requests.utils import requote_uri
from pyrogram import Client, filters
from pyrogram.types import *


load_dotenv()
API = "https://api.abirhasan.wtf/google?query="


Bot = Client(
    "Google-Search-Bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)


START_TEXT = """👋 Hello {}
🥀 I am a Emo Google Search Bot. \
Send a text for google search result.

> `I can search from google. Use me in inline.`

👨‍💻 Devoloper :- @ImRishmika
⚡ Powerd By Emo Network

"""

JOIN_BUTTON = 
[
    InlineKeyboardButton(
        text='⚡Team Emo⚡',
        url='https://telegram.me/EmoBotDevolopers'
    )
],
[
    InlineKeyboardButton(
        text='👨‍💻 Devoloper 👨‍💻',
        url='https://telegram.me/ImRishmika'
    )
],



@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        reply_markup=InlineKeyboardMarkup([JOIN_BUTTON]),
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_message(filters.private & filters.text)
async def filter(bot, update):
    await update.reply_text(
        text="☘ `Click the button below for searching...`",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="💭 Search Here", switch_inline_query_current_chat=update.text)],
                [InlineKeyboardButton(text="👁‍🗨 Search in another chat", switch_inline_query=update.text)]
            ]
        ),
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_inline_query()
async def inline(bot, update):
    results = google(update.query)
    answers = []
    for result in results:
        answers.append(
            InlineQueryResultArticle(
                title=result["title"],
                description=result["description"],
                input_message_content=InputTextMessageContent(
                    message_text=result["text"],
                    disable_web_page_preview=True
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(text="🔗 Link", url=result["link"])],
                        JOIN_BUTTON
                    ]
                )
            )
        )
    await update.answer(answers)


def google(query):
    r = requests.get(API + requote_uri(query))
    informations = r.json()["results"][:50]
    results = []
    for info in informations:
        text = f"🔅 **Title:** `{info['title']}`"
        text += f"\n💬 **Description:** `{info['description']}`"
        text += f"\n\n⚡ Powerd by Emo Network"
        results.append(
            {
                "title": info['title'],
                "description": info['description'],
                "text": text,
                "link": info['link']
            }
        )
    return results


Bot.run()
