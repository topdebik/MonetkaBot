# -*- coding: utf-8 -*-

import asyncio
from telebot.async_telebot import AsyncTeleBot
from random import choices
import datetime
import vk_fetcher
import llama_fetcher
from math import ceil
import consts  # secret constants


async def throw_monetka():
    return choices(
        ["Орёл", "Решка", "Капец повезло повезло монетка упала на ребро"],
        k=1,
        weights=[49.95, 49.95, 0.1],
    )[0]


bot = AsyncTeleBot(consts.TELEGRAM_TOKEN)

horoscope_chat_ids = (
    consts.horoscope_chat_ids
)  # chats to auto send horoscope at midnight


@bot.message_handler(commands=["478_story"])
async def send_horoscope(message):
    if message.chat.id in consts.ban_list:
        return
    await bot.send_chat_action(message.chat.id, action="typing")
    story = await llama_fetcher.get_478_story()
    await bot.reply_to(message, story)
    print(message.chat.id, message.from_user.username, "/478_story")


@bot.message_handler(commands=["horoscope"])
async def send_horoscope(message):
    if message.chat.id in consts.ban_list:
        return
    photos = await vk_fetcher.fetch_horoscopes()
    await bot.send_media_group(message.chat.id, photos)
    print(message.chat.id, message.from_user.username, "/horoscope")


@bot.message_handler(commands=["monetka"])
async def send_monetka(message):
    if message.chat.id in consts.ban_list:
        return
    result = await throw_monetka()
    await bot.reply_to(message, result)
    print(message.chat.id, message.from_user.username, "/monetka", result)


@bot.message_handler(commands=["start", "help"])
async def send_help(message):
    if message.chat.id in consts.ban_list:
        return
    await bot.reply_to(
        message,
        """
Добрый день, я монеткобросатель🫡
/help - Вывести этот туториал
/monetka - бросить монеткy
/horoscope - Вывести гороскоп на сегодня
/478_story - Рассказать историю про 478 автобус
""",
    )
    print(message.chat.id, message.from_user.username, "/help")


@bot.message_handler(func=lambda message: True)
async def ingore_messages(message):
    pass


async def wait_until_new_day():
    dt = datetime.datetime.now()
    tomorrow = dt + datetime.timedelta(days=1)
    sleep_time = ceil(
        (datetime.datetime.combine(tomorrow, datetime.time.min) - dt).total_seconds()
    )
    await asyncio.sleep(sleep_time)  # wait until the beginning of new day


async def run_horoscope_polling():
    while True:
        await wait_until_new_day()
        photos = await vk_fetcher.fetch_horoscopes()
        for chat_id in horoscope_chat_ids:
            await bot.send_media_group(chat_id, photos)
            print(chat_id, "on_time_schedule", "/horoscope")


loop = asyncio.new_event_loop()
loop.create_task(bot.infinity_polling())
loop.create_task(run_horoscope_polling())
loop.run_forever()
