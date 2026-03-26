import random
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

router = Router()

# ========== ЗАДАНИЕ 1: /start с двумя кнопками ==========
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем кнопки
    button1 = KeyboardButton(text="🐶 Собачка")
    button2 = KeyboardButton(text="🐱 Кошечка")
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button1, button2]],
        resize_keyboard=True
    )
    
    await message.answer(
        "Привет! Выбери животное:",
        reply_markup=keyboard
    )

# Обработчик кнопки "Собачка"
@router.message(F.text == "🐶 Собачка")
async def dog_answer(message: types.Message):
    await message.answer("🐕 Гав-гав! Собачка — лучший друг человека!")

# Обработчик кнопки "Кошечка"
@router.message(F.text == "🐱 Кошечка")
async def cat_answer(message: types.Message):
    await message.answer("🐈 Мяу-мяу! Кошечка любит молоко!")


# ========== ЗАДАНИЕ 2: стикер, GIF, ссылка ==========
@router.message(Command("media"))
async def cmd_media(message: types.Message):
    # Стикер (ID стикера, можно взять любой существующий)
    await message.answer_sticker("CAACAgIAAxkBAAEKAAA")
    
    # GIF-анимация (ссылка на гифку)
    await message.answer_animation("https://media.giphy.com/media/3o7abB06u9bNzA8LC8/giphy.gif")
    
    # Ссылка на YouTube
    await message.answer("Смотри видео: https://www.youtube.com/watch?v=dQw4w9WgXcQ")


# ========== ЗАДАНИЕ 3: кнопка приветствия ==========
@router.message(Command("hello"))
async def cmd_hello(message: types.Message):
    button = KeyboardButton(text="👋 Поздороваться")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    await message.answer("Нажми на кнопку:", reply_markup=keyboard)

@router.message(F.text == "👋 Поздороваться")
async def greet(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}! Рад тебя видеть!")


# ========== ЗАДАНИЕ 4: случайное число от 1 до 10 ==========
@router.message(Command("random"))
async def cmd_random(message: types.Message):
    number = random.randint(1, 10)
    await message.answer(f"🎲 Случайное число: {number}")


# ========== ЗАДАНИЕ 5: счетчик (+1 и -1) ==========
# Хранилище для счетчиков пользователей
counters = {}

@router.message(Command("counter"))
async def cmd_counter(message: types.Message):
    user_id = message.from_user.id
    
    # Если у пользователя еще нет счетчика — создаем
    if user_id not in counters:
        counters[user_id] = 0
    
    button_plus = KeyboardButton(text="➕ +1")
    button_minus = KeyboardButton(text="➖ -1")
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_plus, button_minus]],
        resize_keyboard=True
    )
    
    await message.answer(
        f"Текущее значение: {counters[user_id]}\nНажми кнопку:",
        reply_markup=keyboard
    )

@router.message(F.text == "➕ +1")
async def plus_one(message: types.Message):
    user_id = message.from_user.id
    if user_id not in counters:
        counters[user_id] = 0
    counters[user_id] += 1
    await message.answer(f"✅ +1! Теперь: {counters[user_id]}")

@router.message(F.text == "➖ -1")
async def minus_one(message: types.Message):
    user_id = message.from_user.id
    if user_id not in counters:
        counters[user_id] = 0
    counters[user_id] -= 1
    await message.answer(f"✅ -1! Теперь: {counters[user_id]}")


# ========== ЗАДАНИЕ 6: игра-викторина ==========
# Вопросы и ответы
quiz_questions = [
    {"question": "Столица Франции?", "answer": "Париж"},
    {"question": "2 + 2 * 2 = ?", "answer": "6"},
    {"question": "Кто написал 'Война и мир'?", "answer": "Толстой"},
    {"question": "Сколько планет в Солнечной системе?", "answer": "8"},
    {"question": "Как называется наша галактика?", "answer": "Млечный Путь"},
    {"question": "Самый большой океан на Земле?", "answer": "Тихий"},
    {"question": "Сколько цветов в радуге?", "answer": "7"},
    {"question": "Кто нарисовал 'Мону Лизу'?", "answer": "Леонардо да Винчи"},
]

# Хранилище состояний викторины
quiz_state = {}

@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    user_id = message.from_user.id
    # Сбрасываем состояние для пользователя
    quiz_state[user_id] = {
        "current": 0,
        "score": 0
    }
    await ask_question(message, user_id)

async def ask_question(message: types.Message, user_id: int):
    current = quiz_state[user_id]["current"]
    if current >= len(quiz_questions):
        # Викторина закончена
        score = quiz_state[user_id]["score"]
        total = len(quiz_questions)
        await message.answer(
            f"🎉 Викторина окончена!\n"
            f"Твой результат: {score} из {total}\n"
            f"Процент: {score * 100 // total}%"
        )
        del quiz_state[user_id]
        return
    
    # Задаем вопрос
    question = quiz_questions[current]["question"]
    await message.answer(f"❓ Вопрос {current + 1}: {question}")

# Обработчик ответов на вопросы
@router.message()
async def quiz_answer(message: types.Message):
    user_id = message.from_user.id
    
    # Если пользователь не в викторине — игнорируем
    if user_id not in quiz_state:
        return
    
    current = quiz_state[user_id]["current"]
    correct_answer = quiz_questions[current]["answer"]
    
    if message.text.lower().strip() == correct_answer.lower():
        # Правильный ответ
        quiz_state[user_id]["score"] += 1
        await message.answer("✅ Правильно!")
    else:
        # Неправильный ответ
        await message.answer(f"❌ Неправильно! Правильный ответ: {correct_answer}")
    
    # Переходим к следующему вопросу
    quiz_state[user_id]["current"] += 1
    await ask_question(message, user_id)