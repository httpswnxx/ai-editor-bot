from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def result_buttons() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="❤️ Like", callback_data="like"),
            InlineKeyboardButton(text="👎 Dislike", callback_data="dislike")
        ],
        [
            InlineKeyboardButton(text="✖️ O‘chirish", callback_data="delete")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
