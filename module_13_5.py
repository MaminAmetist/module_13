# Клавиатура кнопок
# Задача "Меньше текста, больше кликов":

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Информация')
kb.add(button)
button_2 = KeyboardButton(text='Рассчитать')
kb.add(button_2)


class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Для подсчета суточной нормы калорий нажмите кнопку "Рассчитать".',
                         reply_markup=kb)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Привет! Я бот, помогающий вашему здоровью.', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def set_gender(message):
    await message.answer('Введите свой пол в формате "М/Ж"', reply_markup=kb)
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def set_age(message, state):
    await state.update_data(gender=message.text)
    data = await state.get_data()
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer('Введите свой рост в сантиметрах:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес в килограммах:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    if data['gender'] == 'М' or data['gender'] == 'м':
        norm = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    else:
        norm = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    await message.answer(f'Ваша суточная нома {norm} калорий.')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
