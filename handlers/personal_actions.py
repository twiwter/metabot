from aiogram import types
from dispatcher import dp, bot
from db import BotDB
import config
from string import Template
import handlers.templates.personal_actions_templates as pa
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from handlers.states.UsersStates import Help
import os

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    """Getting Started"""
    database = BotDB(os.environ.get("HOST"), os.environ.get("USER"), os.environ.get("PASSWORD"), os.environ.get("DB"))
    if(database.user_exist(message.from_user.id)):
        user_information = database.get_user_information(message.from_user.id)
        await message.answer(pa.start.substitute(name=user_information[2]))
    else:
        await message.reply("Вибачай, друже, але тобі цей бот недоступний )")

@dp.message_handler(commands=['info'])
async def process_information_command(message: types.Message):
    """Informing the user"""
    database = BotDB(os.environ.get("HOST"), os.environ.get("USER"), os.environ.get("PASSWORD"), os.environ.get("DB"))
    if(database.user_exist(message.from_user.id)):
        await message.answer(pa.info, parse_mode="Markdown")
    else:
        await message.reply("Вибачай, друже, але тобі цей бот недоступний )")

@dp.message_handler(commands=['profile'])
async def process_profile_command(message: types.Message):
    """Displaying the user profile"""
    database = BotDB(os.environ.get("HOST"), os.environ.get("USER"), os.environ.get("PASSWORD"), os.environ.get("DB"))
    if(database.user_exist(message.from_user.id)):
        if(message.from_user.id == 447002854):
            await message.answer("Ти батько, навіщо тобі дивитися свій профіль?)")
        elif(message.from_user.id == 712140726):
            await message.answer("Не треба так ...")
        else:
            profile_data = database.get_user_information(message.from_user.id)
            await message.answer(pa.profile.substitute(
                name=profile_data[2], 
                team_name=profile_data[3], 
                score=profile_data[6], 
                clients_count=profile_data[4], 
                consults_count=profile_data[5])
            )
            
    else:
        await message.reply("Вибачай, друже, але тобі цей бот недоступний )")

@dp.message_handler(commands=['confrontation'])
async def process_confrontation_command(message: types.Message):
    """Print all info about both teams"""
    database = BotDB(os.environ.get("HOST"), os.environ.get("USER"), os.environ.get("PASSWORD"), os.environ.get("DB"))
    if(database.user_exist(message.from_user.id)):
        if(message.from_user.id == 447002854):
            await message.answer("Це тобі не потрібно )")
        elif(message.from_user.id == 712140726):
            await message.answer("Не треба так ...")
        else:
            score_blue = database.get_score_team("🧢 Аватар")
            clients_count_blue = database.get_clients_count_team("🧢 Аватар")
            consults_count_blue = database.get_consults_count_team("🧢 Аватар")

            score_red = database.get_score_team("🔴 Криптопанк")
            clients_count_red = database.get_clients_count_team("🔴 Криптопанк")
            consults_count_red = database.get_consults_count_team("🔴 Криптопанк")

            last_operation = database.get_last_operation()
            await message.answer(type(last_operation))

            if (last_operation != []):
                user_info = database.get_user_information(last_operation[1])
                operation = last_operation[2]

                if (operation == "stories"):
                    text = f"користувач *{user_info[2]}* з команди `{user_info[3]}` зробив сторіс"
                elif (operation == "sendout"):
                    text = f"користувач *{user_info[2]}* з команди `{user_info[3]}` зробив розсилку"
                elif (operation == "client"):
                    text = f"користувач *{user_info[2]}* з команди `{user_info[3]}` закрив клієнта {last_operation[3]} на чек {last_operation[4]}$"
                elif (operation == "consult"):
                    text = f"користувач *{user_info[2]}* з команди `{user_info[3]}` провів консультацію для {last_operation[3]} на чек {last_operation[4]}$"
            else:
                text = "бот був створений"

            await message.answer(pa.confrontation_text.substitute(
                score_blue=score_blue,
                score_red=score_red,
                client_blue=clients_count_blue,
                consult_blue=consults_count_blue,
                client_red=clients_count_red,
                consult_red=consults_count_red,
                last_operation_text=text
            ), parse_mode="Markdown")

    else:
        await message.reply("Вибачай, друже, але тобі цей бот недоступний )")

@dp.message_handler(commands=['intelligence'])
async def process_intelligence_command(message: types.Message):
    """Print all info about team"""
    database = BotDB(os.environ.get("HOST"), os.environ.get("USER"), os.environ.get("PASSWORD"), os.environ.get("DB"))
    if(database.user_exist(message.from_user.id)):
        if(message.from_user.id == 447002854):
            await message.answer("І це тобі теж не потрібно )")
        elif(message.from_user.id == 712140726):
            await message.answer("Не треба так ...")
        else:
            user_info = database.get_user_information(message.from_user.id)
            team_info = database.get_all_users_team_info(user_info[3])
            text = f"{team_info[0][3]}и\n\n"
            
            for line in team_info:
                # print(line) #(5, 423579650, 'Олександр', '🧢 Аватар', 1, 1, 60) (7, 336334413, 'Ірина', '🧢 Аватар', 0, 0, 0)
                text += f"👤 [{line[2]}](tg://user?id={line[1]}):\n\n🎖 Кількість балів: {line[-1]}\n💸 Клієнтів: {line[-3]}\n🥸 Консультацій: {line[-2]}\n\n"

            await message.answer(text, parse_mode="Markdown")
    else:
        await message.reply("Вибачай, друже, але тобі цей бот недоступний )")

@dp.message_handler(commands=['help'])
async def process_intelligence_command(message: types.Message):
    """Contacting Support"""
    database = BotDB(os.environ.get("HOST"), os.environ.get("USER"), os.environ.get("PASSWORD"), os.environ.get("DB"))
    if(database.user_exist(message.from_user.id)):
        if(message.from_user.id != 447002854):
            await message.reply("Йой, вийшла помилка ... Напиши що сталося?")
            await Help.message_help.set()
        else:
            await message.answer("Краще в приватні пиши")
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

@dp.message_handler(state=Help.message_help)
async def process_name(message: types.Message, state: FSMContext):
    database = BotDB(os.environ.get("HOST"), os.environ.get("USER"), os.environ.get("PASSWORD"), os.environ.get("DB"))
    user = database.get_user_information(message.from_user.id)
    name = user[2]
    chat_id = user[1]

    await bot.send_message(423579650, f"*⚠️ Повідомлення про помилку від {name} {chat_id}*\n\n{message.text}", parse_mode="Markdown")
    await message.reply("Інформація вже в дорозі!")
    await state.finish()