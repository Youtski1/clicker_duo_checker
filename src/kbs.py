from aiogram.types import InlineKeyboardButton as ibut
from aiogram.utils.keyboard import InlineKeyboardBuilder as builder

def kb_start_webapp():
    return builder([[
        ibut(text="😈 бить 😈", url="http://192.168.100.8:3000")
    ]]).as_markup()
