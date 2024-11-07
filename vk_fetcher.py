# -*- coding: utf-8 -*-

from vk import API
from telebot.types import InputMediaPhoto
from datetime import date
from PIL import Image
from pytesseract import image_to_string
import requests
from io import BytesIO
import consts  # secret constants

TOKEN = consts.VK_TOKEN
MONTHS = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
]

HOROSCOPES = ["дева", "лева", "лев", "рак", "овен", "скорпион", "весы", "весь]"]


async def fetch_horoscopes():
    vk = API(access_token=TOKEN, v="5.131")

    posts = vk.wall.get(owner_id="-182875281", count=20)["items"]

    current_date = date.today()
    current_month = MONTHS[current_date.month - 1]
    current_day = current_date.day

    posts = [
        post
        for post in posts
        if (f"Гороскоп на {current_day} {current_month}" in post["text"])
    ]

    if len(posts) == 0:
        return None

    photo_urls = []
    for post in posts:
        photo_objects = [
            attachment_object
            for attachment_object in post["attachments"]
            if attachment_object["type"] == "photo"
        ]
        photo_urls_in_post = [
            photo_object["photo"]["orig_photo"]["url"] for photo_object in photo_objects
        ]
        photo_urls.extend(photo_urls_in_post)

    photos = []
    for photo_url in photo_urls:
        response = requests.get(photo_url)
        photos.append(BytesIO(response.content))

    photos_to_send = []
    for photo in photos:
        image = Image.open(photo)
        image_text = (
            image_to_string(image, lang="rus")
            .replace(" ", "")
            .replace("\n", "")
            .lower()[:20]
        )

        for horoscope_name in HOROSCOPES:
            if horoscope_name in image_text:
                buf = BytesIO()
                image.save(buf, format="JPEG")
                photos_to_send.append(InputMediaPhoto(media=buf.getvalue()))
                break

    return photos_to_send
