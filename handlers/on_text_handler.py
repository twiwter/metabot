from aiogram import types
from dispatcher import dp, bot
from db import BotDB
import config
from string import Template
import handlers.templates.personal_actions_templates as pa
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import re
import os

from handlers.sheets import send_values_to_table

from handlers.states.UsersStates import Stories, Client, Consult, SendOut



@dp.message_handler(content_types="text")
async def user_messages(message: types.Message):
    database = BotDB(os.environ.get("HOST"), os.environ.get("USER"), os.environ.get("PASSWORD"), os.environ.get("DB"))
    if(database.user_exist(message.from_user.id)):
        if(message.from_user.id != 447002854 and message.from_user.id != 712140726):
            text = re.sub(r'[^\w\s]','', message.text).lower()
            keys = ["сторіс", "клієнт", "консультація", "консультацію", "клієнтa", "розсилка", "розсилку"]

            crew = ""

            for key in keys:
                if key in text:
                    crew = key
                    break
            
            if crew == "сторіс":
                await message.reply("Молодець 👏 Сторіс важлива частина побудови особистого бренду, так тримати!\n\nВідправ боту скріншот твоєї історії з програми Instagram 👇")
                await Stories.photo.set()
            elif crew in ["розсилка", "розсилку"]:
                await message.reply("Молодець 👏 Розсилка це один із методів пошуку клієнтів, не потрібно його ігнорувати)\n\nВідправ кількість розсилок, яку ти зробив за сьогодні 👇")
                await SendOut.count.set()
            elif crew in ["клієнт", "клієнтa"]:
                await message.reply("Та ну! А ну хвалися!\n\nВідправ посилання на клієнта 👇")
                await Client.link.set()
            elif crew in ["консультація", "консультацію"]:
                await message.reply("Вже проводиш особисті консультації? Моя ти радість )\n\nВідправ посилання на клієнта 👇")
                await Consult.link.set()
            else:
                await message.reply("що?")
        else:
            await message.reply("Та не, не треба )")

    else:
        await message.reply("Вибачай, друже, але тобі цей бот недоступний )")

# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """Allow user to cancel any action"""
    current_state = await state.get_state()
    if current_state is None:
        return

    await message.reply('Відхилено.', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

# Stories
@dp.message_handler(lambda message: message.content_type != "photo", state=Stories.photo)
async def process_content_type_invalid(message: types.Message):
    await message.reply("Я говорив фото! 😡 \nНаступного разу зніму 1 бал! \n\nВідправ боту СКРІНШОТ твоєї історії з програми Instagram 👇")

@dp.message_handler(content_types=["photo"], state=Stories.photo)
async def process_stories(message: types.Message, state: FSMContext):
    database = BotDB(os.environ.get("HOST"), os.environ.get("USER"), os.environ.get("PASSWORD"), os.environ.get("DB"))
    user_id = message.from_user.id
    operation_name = "сторис"
    score = 1

    database.add_operation(user_id, "stories", score)
    data = database.get_user_information(user_id)
    database.update_score(user_id, 1)

    table_name = f"{data[2]}_{user_id}"

    # send_values_to_table(table_name, operation_name, score)

    await message.answer("Фото отримано! ✅ \n\nТобі нараховується 1 бал! 🎖")
    await state.finish()

# SendOut
@dp.message_handler(lambda message: not message.text.isdigit(), state=SendOut.count)
async def process_content_invalid(message: types.Message):
    await message.reply("Надіслано невірне значення! Відправ ще раз!")

@dp.message_handler(state=SendOut.count)
async def process_count_send_out(message: types.Message, state: FSMContext):
    count = int(message.text)
    database = BotDB(os.environ.get("HOST"), os.environ.get("USER"), os.environ.get("PASSWORD"), os.environ.get("DB"))
    if (count < 10):
        await message.answer("Це дуже мало...")
    else:
        score = count // 10 * 3

        user_id = message.from_user.id
        operation_name = "рассылка"

        database.add_operation(user_id, "sendout", score)
        database.update_score(user_id, score)
        data = database.get_user_information(user_id)

        table_name = f"{data[2]}_{user_id}"
        send_values_to_table(table_name, operation_name, score)

        await message.answer(f"Отримано! ✅ \n\nТобі нараховується {score} бал! 🎖")

    await state.finish()

# Client
@dp.message_handler(state=Client.link)
async def process_client_link(message: types.Message, state: FSMContext):
    await Client.next()
    async with state.proxy() as data:
        data['link'] = message.text

    await message.answer("А тепер чек, хвались ))\nЦіну пиши в $$$ 👇")

@dp.message_handler(lambda message: not message.text.isdigit(), state=Client.amount)
async def process_content_invalid(message: types.Message):
    await message.reply("Надіслано неправильну суму! Відправ ще раз!")

@dp.message_handler(lambda message: int(message.text) <= 0, state=Client.amount)
async def process_content_invalid(message: types.Message):
    await message.reply("Надіслано неправильну суму! Відправ ще раз!")

@dp.message_handler(state=Client.amount)
async def process_client_amount(message: types.Message, state: FSMContext):
    database = BotDB(os.environ.get("HOST"), os.environ.get("USER"), os.environ.get("PASSWORD"), os.environ.get("DB"))
    async with state.proxy() as data:
        data['amount'] = int(message.text)

    if (data['amount'] > 0 and data['amount'] < 100):
        score = 20
    elif (data['amount'] >= 100 and data['amount'] < 200):
        score = 30
    elif (data['amount'] >= 200 and data['amount'] <= 300):
        score = 40
    elif (data['amount'] > 300):
        score = 50

    user_id = message.from_user.id
    operation_name = "клиент"

    # print(data) # FSMContextProxy state = 'Client:amount', data = {'link': 'посилання', 'amount': 200}, closed = True

    database.add_operation(user_id, "client", score, data["link"], data["amount"])
    database.update_score(user_id, score)
    database.update_clients_count(user_id, 1)
    user_info = database.get_user_information(user_id)

    table_name = f"{user_info[2]}_{user_id}"
    print(data)

    link = str(data["link"])
    amount = int(data["amount"])

    send_values_to_table(table_name, operation_name, score, link, amount)

    await message.answer(f"Отримано! ✅ \n\nТобі нараховується {score} балів! 🏆")

    await state.finish() 

    # database.add_operation(user_id, "sendout", score, data['age'])

# Consult
@dp.message_handler(state=Consult.link)
async def process_consult_link(message: types.Message, state: FSMContext):
    await Consult.next()
    async with state.proxy() as data:
        data['link'] = message.text

    await message.answer("А тепер чек, хвались ))\nЦіну пиши в $$$ 👇")

@dp.message_handler(lambda message: not message.text.isdigit(), state=Consult.amount)
async def process_content_invalid(message: types.Message):
    await message.reply("Надіслано неправильну суму! Відправ ще раз!")

@dp.message_handler(lambda message: int(message.text) <= 0, state=Consult.amount)
async def process_content_invalid(message: types.Message):
    await message.reply("Надіслано неправильну суму! Відправ ще раз!")

@dp.message_handler(state=Consult.amount)
async def process_consult_amount(message: types.Message, state: FSMContext):
    database = BotDB(os.environ.get("HOST"), os.environ.get("USER"), os.environ.get("PASSWORD"), os.environ.get("DB"))
    async with state.proxy() as data:
        data['amount'] = int(message.text)

    if (data['amount'] == 0):
        score = 5
    elif (data['amount'] > 0 and data['amount'] < 30):
        score = 10
    elif (data['amount'] >= 30 and data['amount'] < 60):
        score = 15
    elif (data['amount'] >= 60 and data['amount'] <= 100):
        score = 20
    elif (data['amount'] > 101):
        score = 30

    user_id = message.from_user.id
    operation_name = "консультация"

    # print(data) # FSMContextProxy state = 'Client:amount', data = {'link': 'посилання', 'amount': 200}, closed = True

    database.add_operation(user_id, "consult", score, data["link"], data["amount"])
    database.update_score(user_id, score)
    database.update_consults_count(user_id, 1)
    user_info = database.get_user_information(user_id)

    table_name = f"{user_info[2]}_{user_id}"
    print(data)

    link = str(data["link"])
    amount = int(data["amount"])

    # send_values_to_table(table_name, operation_name, score, link, amount)

    await message.answer(f"Отримано! ✅ \n\nТобі нараховується {score} балів! 🏆")

    await state.finish() 

    # database.add_operation(user_id, "sendout", score, data['age'])
