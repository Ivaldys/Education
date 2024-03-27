from aiogram import  Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.types import ( CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage, Redis
from config_data.config import load_config
import lexiconn.lexicon_ru
from keyboards.set_menu import set_main_menu
from keyboards.user_keyboards import create_inline_kb
import use_database.using_database
import use_database.client_information
import use_database.teacher_information
import sqlite3

# Инициализируем роутер уровня модуля
router = Router()
config = load_config()

bot = Bot(token=config.tg_bot.token)

redis = Redis(host='localhost')

storage = RedisStorage(redis=redis)

user_dict: dict[int, dict[str, str | int | bool]] = {}

class FSMFillForm(StatesGroup):
    client_login = State()
    cl_name = State()
    cl_surname  = State()
    cl_course  = State()
    cl_phone  = State()
    cl_mail  = State()
    cl_university  = State()
    cl_faculty  = State()
    teacher_login  = State()
    th_name  = State()
    th_surname  = State()
    th_course  = State()
    th_phone  = State()
    th_mail  = State()
    th_university  = State()
    th_faculty  = State()

# Этот хэндлер будет срабатывать на команду "/start"
@router.message(Command(commands=["start"]),  StateFilter(default_state))
async def process_start_command(message: Message):
    keyboard = create_inline_kb(2, 'but_1', 'but_2')
    date = message.date
    await bot.send_photo(message.chat.id, lexiconn.lexicon_ru.photo_url, caption = lexiconn.lexicon_ru.lexicon_start + str(date), reply_markup=keyboard)
    await set_main_menu(bot)

# Этот хэндлер будет срабатывать на команду "/help"
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer( '💩💩💩')

@router.message(Command(commands=['contact']))
async def process_contact_command(message: Message):
    user_id = message.from_user.id
    await message.answer(f'Ваш ID: {user_id}')

@router.message(Command(commands=['exit']))
async def process_exit_command(message: Message,  state: FSMContext):
    await state.set_state(default_state)

@router.callback_query(F.data == 'but_1',  StateFilter(default_state))
async def process_button_client_press(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    result = use_database.using_database.check_clients_authorization(str(user_id))
    keyboard = create_inline_kb(1, 'but_5','but_6','but_7','but_8')
    if (result):
        await bot.send_photo(callback.message.chat.id, lexiconn.lexicon_ru.client_photo_url, caption = lexiconn.lexicon_ru.cl_login_text(use_database.client_information.clients_name(str(user_id))), reply_markup=keyboard)
        await state.set_state(FSMFillForm.client_login)

    else:
        await bot.send_message(callback.message.chat.id, 'Для начала вам нужно зарегистрироваться!\nВведите пожалуйста ваше Имя')
        await state.set_state(FSMFillForm.cl_name)
        use_database.using_database.new_client(user_id,callback.from_user.username)

#Вводим имя клиента
@router.message(StateFilter(FSMFillForm.cl_name))
async def fill_client_name(message: Message, state: FSMContext):
    use_database.using_database.fill_clients_name(message.from_user.id, message.text)
    await bot.send_message(message.chat.id, 'Отлично, введите вашу Фамилию:')
    await state.set_state(FSMFillForm.cl_surname)

#Вводим фамилию клиента
@router.message(StateFilter(FSMFillForm.cl_surname))
async def fill_client_surname(message: Message, state: FSMContext):
    use_database.using_database.fill_clients_surname(message.from_user.id, message.text)
    await bot.send_message(message.chat.id, 'Введите ваш курс в унике:')
    await state.set_state(FSMFillForm.cl_course)

#Вводим курс клиента
@router.message(StateFilter(FSMFillForm.cl_course))
async def fill_client_course(message: Message, state: FSMContext):
    use_database.using_database.fill_clients_course(message.from_user.id, message.text)
    await bot.send_message(message.chat.id, 'Введите ваш номер телефона:')
    await state.set_state(FSMFillForm.cl_phone)

#Вводим телефон клиента
@router.message(StateFilter(FSMFillForm.cl_phone))
async def fill_client_phone(message: Message, state: FSMContext):
    use_database.using_database.fill_clients_phone(message.from_user.id, message.text)
    await bot.send_message(message.chat.id, 'Введите вашу электронную почту:')
    await state.set_state(FSMFillForm.cl_mail)

#Вводим почту клиента
@router.message(StateFilter(FSMFillForm.cl_mail))
async def fill_client_mail(message: Message, state: FSMContext):
    use_database.using_database.fill_clients_mail(message.from_user.id, message.text)
    keyboard = create_inline_kb(1, 'but_3')
    await bot.send_message(message.chat.id, 'Выберите ваш университет:', reply_markup= keyboard)
    await state.set_state(FSMFillForm.cl_university)

#Выбираем ВУЗ для клиента
@router.callback_query(F.data == 'but_3',  StateFilter(FSMFillForm.cl_university))
async def fill_client_university(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    use_database.using_database.fill_clients_university(callback.from_user.id, callback.data)
    keyboard = create_inline_kb(1, 'but_4')
    await bot.send_message(callback.message.chat.id, 'Выберите ваш факультет:', reply_markup= keyboard)
    await state.set_state(FSMFillForm.cl_faculty)


#Выбираем факультет для клиента
@router.callback_query(F.data == 'but_4',  StateFilter(FSMFillForm.cl_faculty))
async def fill_client_faculty(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    keyboard = create_inline_kb(1, 'but_cl_menu')
    use_database.using_database.fill_clients_faculty(callback.from_user.id, callback.data)
    await bot.send_message(callback.message.chat.id, 'Регистрация прошла успешно!\n      Добро пожаловать', reply_markup= keyboard)
    await state.set_state(FSMFillForm.client_login)


#Вход учителя
@router.callback_query(F.data == 'but_2',  StateFilter(default_state))
async def process_button_teacher_press(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    result = use_database.using_database.check_teachers_authorization(str(user_id))
    keyboard = create_inline_kb(1, 'but_5', 'but_18','but_8')
    if (result):
        await bot.send_photo(callback.message.chat.id, lexiconn.lexicon_ru.teacher_photo_url, caption = lexiconn.lexicon_ru.th_login_text(use_database.teacher_information.teacher_name(str(user_id))), reply_markup= keyboard)
        await state.set_state(FSMFillForm.teacher_login)

    else:
        await bot.send_message(callback.message.chat.id, 'Для начала вам нужно зарегистрироваться!\nВведите пожалуйста ваше Имя')
        await state.set_state(FSMFillForm.th_name)
        use_database.using_database.new_teacher(user_id,callback.from_user.username)



#Вводим имя учителя
@router.message(StateFilter(FSMFillForm.th_name))
async def fill_teacher_name(message: Message, state: FSMContext):
    use_database.using_database.fill_teachers_name(message.from_user.id, message.text)
    await bot.send_message(message.chat.id, 'Отлично, введите вашу Фамилию:')
    await state.set_state(FSMFillForm.th_surname)

#Вводим фамилию учителя
@router.message(StateFilter(FSMFillForm.th_surname))
async def fill_teacher_surname(message: Message, state: FSMContext):
    use_database.using_database.fill_teachers_surname(message.from_user.id, message.text)
    await bot.send_message(message.chat.id, 'Введите ваш курс в унике:')
    await state.set_state(FSMFillForm.th_course)

#Вводим курс учителя
@router.message(StateFilter(FSMFillForm.th_course))
async def fill_teacher_course(message: Message, state: FSMContext):
    use_database.using_database.fill_teachers_course(message.from_user.id, message.text)
    await bot.send_message(message.chat.id, 'Введите ваш номер телефона:')
    await state.set_state(FSMFillForm.th_phone)

#Вводим телефон учителя
@router.message(StateFilter(FSMFillForm.th_phone))
async def fill_teacher_phone(message: Message, state: FSMContext):
    use_database.using_database.fill_teachers_phone(message.from_user.id, message.text)
    await bot.send_message(message.chat.id, 'Введите вашу электронную почту:')
    await state.set_state(FSMFillForm.th_mail)

#Вводим почту учителя
@router.message(StateFilter(FSMFillForm.th_mail))
async def fill_teacher_mail(message: Message, state: FSMContext):
    use_database.using_database.fill_teachers_mail(message.from_user.id, message.text)
    keyboard = create_inline_kb(1, 'but_3')
    await bot.send_message(message.chat.id, 'Выберите ваш университет:', reply_markup= keyboard)
    await state.set_state(FSMFillForm.th_university)

#Выбираем ВУЗ для учителя
@router.callback_query(F.data == 'but_3',  StateFilter(FSMFillForm.th_university))
async def fill_teacher_university(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    use_database.using_database.fill_teachers_university(callback.from_user.id, callback.data)
    keyboard = create_inline_kb(1, 'but_4')
    await bot.send_message(callback.message.chat.id, 'Выберите ваш факультет:', reply_markup= keyboard)
    await state.set_state(FSMFillForm.th_faculty)


#Выбираем факультет для учителя
@router.callback_query(F.data == 'but_4',  StateFilter(FSMFillForm.th_faculty))
async def fill_teacher_faculty(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    keyboard = create_inline_kb(1, 'but_th_menu')
    use_database.using_database.fill_teachers_faculty(callback.from_user.id, callback.data)
    await bot.send_message(callback.message.chat.id, 'Регистрация прошла успешно!\n      Добро пожаловать', reply_markup= keyboard)
    await state.set_state(FSMFillForm.teacher_login)
