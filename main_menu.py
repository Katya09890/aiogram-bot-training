from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def get_main_menu():
    buttons = [
        [KeyboardButton(text="🎲 Случайное число")],
        [KeyboardButton(text="🔢 Счетчик")],
        [KeyboardButton(text="🎮 Викторина")],
        [KeyboardButton(text="🖼️ Медиа")],
        [KeyboardButton(text="👋 Приветствие")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)