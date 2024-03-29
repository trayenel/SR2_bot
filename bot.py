from helper_functions import validateUrl, setLanguage, extractUrl
import logging
from lang_constants import START_MESSAGE, HELP_MESSAGE, URL_ERR_MESSAGE
from pyrogram import Client, filters, idle
from pyrogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


async def login(name, API_ID, API_HASH, BOT_TOKEN):
    app = Client(name, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

    @app.on_message(filters.command(["start"]) & filters.private)
    async def startHandler(client, message):
        await app.send_message(message.chat.id, _(START_MESSAGE))

    @app.on_message(filters.command(["help"]) & filters.private)
    async def helpHandler(client, message):
        await app.send_message(message.chat.id, _(HELP_MESSAGE))

    @app.on_message(filters.command(["lang"]) & filters.private)
    async def langHandler(client, message):
        await app.send_message(
            message.chat.id,
            "Lang",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🇷🇴", callback_data="ro"),
                        InlineKeyboardButton("🇷🇺", callback_data="ru"),
                        InlineKeyboardButton("🇬🇧", callback_data="en"),
                    ]
                ]
            ),
        )

    @app.on_callback_query()
    async def answer(client, callback_query):
        setLanguage(callback_query.data)

    @app.on_message(filters.private)
    async def domainHandler(client, message):
        if not validateUrl(message.text):
            await app.send_message(
                message.chat.id,
                _(URL_ERR_MESSAGE),
            )
            return
        await app.send_message(message.chat.id, extractUrl(message.text))

    await app.start()

    logging.getLogger("SR2_bot").info("Auth successful")

    await idle()

    await app.stop()
