from aiogram.dispatcher.filters.state import StatesGroup, State

class AdminMessagesStates(StatesGroup):
    message_warning = State() # Will be represented in storage as 'Form:message_warning'
    message_information = State() # Will be represented in storage as 'Form:message_information'