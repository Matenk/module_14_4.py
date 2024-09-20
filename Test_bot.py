from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from admin import *
from db import *
from crud_functions import *
from key import API
from aiogram.dispatcher import FSMContext
import asyncio
from keyboards import *
from texts import *
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())




class UserState(StatesGroup):

    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer(age_)
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    if not message.text.isdigit() or not (
            0 < int(message.text) < 120):
        await message.answer('Пожалуйста, введите корректный возраст (число от 1 до 120).')
        return
    await state.update_data(age=message.text)
    if int(message.text) % 10 == 1 and int(message.text) % 100 != 11:
        word = 'год'
    elif int(message.text) % 100 in [2, 3, 4] and int(message.text) % 100 not in [12, 13, 14]:
        word = 'года'
    else:
        word = 'лет'
    await message.answer(f'Целых {message.text} {word}...и как ты справляешься с такими высокими технологиями в твоем-то возрасте? {growth_}')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    if not message.text.isdigit() or not (50 < int(message.text) < 300):
        await message.answer('Пожалуйста, введите корректный рост (число от 50 до 300 сантиметров).')
        return
    await state.update_data(growth=message.text)
    await message.answer(weight_)
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    if not message.text.isdigit() or not (20 < int(message.text) < 300):
        await message.answer('Пожалуйста, введите корректный вес (число от 20 до 300 кг).')
        return
    await state.update_data(weight=message.text)
    data = await state.get_data()
    w = data["weight"]
    g = data["growth"]
    a = data["age"]
    calories = 10 * int(w) + int(6.25) * int(g) - 5 * int(a) + 5
    await message.answer(f'Ууу, дорогуша, твоя суточная норма ккал: {calories}, крч столько сколько ты съела сегодня на завтрак...\n Пока!')
    await state.finish()

products = get_all_products()
@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for product in products:
        id, title, description, price = product
        image_path = f'img/{title.lower()}.jpg'
        with open(image_path, 'rb') as file:
            await message.answer_photo(file, caption=f' {title} | {description} | {price}\n')

    await message.answer('Выберите продукцию', reply_markup=kb_catalog)



@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(buy_complete)
    await call.answer()

@dp.callback_query_handler(text='other')
async def other_mes(call):
    await call.message.answer(other)
    await call.answer()



@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(formula)
    await call.answer()



@dp.message_handler(text='Расчет')
async def main_menu(message):
    await message.answer('Выбери опцию', reply_markup=kb2)

@dp.message_handler(text='Информация')
async def info(message):
    await message.answer(all_info)



@dp.message_handler(commands=['start'])
async def start_message(message):
    with open('img/hello.jpg', 'rb') as file:
        await message.answer_photo(file, caption=f'Привет, {message.from_user.username.capitalize()}! ' + start, reply_markup=start_kb)



@dp.message_handler()
async def all(message):
    await message.answer(all_mess)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
