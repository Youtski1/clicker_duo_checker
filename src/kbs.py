from aiogram.types import InlineKeyboardButton as ibut
from aiogram.utils.keyboard import InlineKeyboardBuilder as builder
from os import environ


LINK_WEB_APP = environ.get("LINK_WEB_URL")

def kb_start_webapp():
    return builder([[
        ibut(text="😈 бить 😈", url=LINK_WEB_APP)
    ]]).as_markup()
