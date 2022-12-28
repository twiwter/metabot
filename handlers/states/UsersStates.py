from aiogram.dispatcher.filters.state import StatesGroup, State

class Help(StatesGroup):
    message_help = State() # Will be represented in storage as 'Form:message_help'

class Stories(StatesGroup):
    photo = State()

class SendOut(StatesGroup):
    count = State()

class Client(StatesGroup):
    link = State()
    amount = State()

class Consult(StatesGroup):
    link = State()
    amount = State()