# -*- coding: utf-8 -*-

from vk import API
from telebot.types import InputMediaPhoto
from datetime import date
from PIL import Image
from pytesseract import image_to_string
import requests
import asyncio
from io import BytesIO
import time
import consts  # secret constants

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

HOROSCOPES = consts.horoscopes  # horoscopes to filter


async def fetch_horoscopes():
    try:
        vk = API(access_token=consts.VK_TOKEN, v="5.131")

        posts = vk.wall.get(owner_id="-182875281", count=20)["items"]
    except:
        consts.update_token()  # secret function to avoid VK fixing this

        vk = API(access_token=consts.VK_TOKEN, v="5.131")

        posts = vk.wall.get(owner_id="-182875281", count=20)["items"]
    await asyncio.sleep(0)

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
        await asyncio.sleep(0)
        photos.append(BytesIO(response.content))

    photos_to_send = []
    photo_num = 0
    for photo in photos:
        image = Image.open(photo)
        processed_image = image.point(lambda x: x > 220 and 255)
        image_width, image_height = processed_image.size
        crop_box = (
            image_width // 7,
            image_height // 18,
            image_width // 6 * 4,
            image_height // 19 * 3,
        )
        processed_image = processed_image.crop(crop_box)

        image_text = (
            image_to_string(processed_image, lang="rus")
            .replace(" ", "")
            .replace("\n", "")
            .lower()[:20]
        )
        await asyncio.sleep(0)

        for horoscope_name in HOROSCOPES:
            if horoscope_name in image_text:
                buf = BytesIO()
                image.save(buf, format="JPEG")
                photos_to_send.append(InputMediaPhoto(media=buf.getvalue()))
                break
        photo_num += 1

    return photos_to_send
