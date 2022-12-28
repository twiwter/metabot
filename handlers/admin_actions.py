from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from dispatcher import dp, bot
import config
from db import BotDB

from handlers.states.AdminStates import AdminMessagesStates

database = BotDB("database.db")

@dp.message_handler(commands=['do_sql'])
async def process_start_command(message: types.Message):
    if (message.from_user.id == 423579650):
        req = database.do_sql(message.text[8:])
        if "SELECT" in message.text[8:]:
            await message.answer(req)
        else:
            await message.reply("Done!")

@dp.message_handler(commands=['get_id'])
async def process_start_command(message: types.Message):
    if (message.from_user.id == 423579650):
        req = database.get_all_users()
        text=""

        for i in req:
            text+=f"{i}\n"
        await message.answer(text)

@dp.message_handler(commands=['warning'])
async def process_start_command(message: types.Message):
    """Send warning message to users"""
    if (message.from_user.id in [423579650, 447002854, 712140726]):
        await message.answer("Надішли мені повідомлення про попередження 👇")
        await AdminMessagesStates.message_warning.set()

@dp.message_handler(commands=['information'])
async def process_start_command(message: types.Message):
    """Send information message to users"""
    if (message.from_user.id in [423579650, 447002854, 712140726]):
        await message.answer("Надішли мені повідомлення про про інформацію 👇")
        await AdminMessagesStates.message_information.set()

@dp.message_handler(commands=['teams'])
async def process_start_command(message: types.Message):
    """Get all infos about teams"""
    if (message.from_user.id in [423579650, 447002854, 712140726]):
        team_blue = database.get_all_users_team_info("🧢 Аватар")
        team_red  = database.get_all_users_team_info("🔴 Криптопанк")

        team_blue_info = "🧢 Аватари\n\n"
        team_red_info  = "🔴 Криптопанки\n\n"

        for team_user in team_blue:
            team_blue_info+=f"👤 {team_user[2]}:\n\n🎖 Кількість балів: {team_user[-1]}\n💸 Клієнтів: {team_user[-3]}\n🥸 Консультацій: {team_user[-2]}\n\n"
        for team_user in team_red:
            team_red_info+=f"👤 {team_user[2]}:\n\n🎖 Кількість балів: {team_user[-1]}\n💸 Клієнтів: {team_user[-3]}\n🥸 Консультацій: {team_user[-2]}\n\n"

        await message.answer(team_blue_info)
        await message.answer(team_red_info)

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

@dp.message_handler(state=AdminMessagesStates.message_warning)
async def process_name(message: types.Message, state: FSMContext):
    """Process message warning"""
    users_id = database.get_all_users_id()
    for user_id in users_id:
        try:
            await bot.send_message(user_id, f"⚠️ *УВАГА ПОПЕРЕДЖЕННЯ* ⚠️\n\n{message.text}", parse_mode="Markdown")
        except:
            pass

    await state.finish()

@dp.message_handler(state=AdminMessagesStates.message_information)
async def process_name(message: types.Message, state: FSMContext):
    """Process message information"""

    users_id = database.get_all_users_id()
    for user_id in users_id:
        try:
            await bot.send_message(user_id, f"📃 Інформація\n\n{message.text}", parse_mode="Markdown")
        except:
            pass
    
    await state.finish()