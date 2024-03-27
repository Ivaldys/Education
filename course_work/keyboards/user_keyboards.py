from aiogram.filters.callback_data import CallbackData
from aiogram.types import ( CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexiconn.lexicon_ru import BUTTONS
import use_database.post_information
import use_database.teacher_information

def create_inline_kb(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=BUTTONS[button] if button in BUTTONS else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


class PostsCallbackFactory(CallbackData, prefix="post"):
    post_id: int
    post_theme: str

class TeacherCallbackFactory(CallbackData, prefix="th"):
    teacher_id: int
    teacher_name: str

class ReviewCallbackFactory(CallbackData, prefix="rw"):
    review: str
    grade: float

def create_buttons_reviews(width: int, reviews, id):
    diction = {key: value for key, value in reviews}
    th_id = use_database.post_information.get_teacher_page_review(id)
    th_tg_id = use_database.teacher_information.teacher_tg_id(th_id)
    th_name = use_database.teacher_information.teacher_name(th_tg_id)
    page = use_database.post_information.get_page_review(id)
    max = use_database.post_information.get_max_page_review(id)
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for key, value in diction.items():
        if (len(key) < 10):
            text1 = key + ' ⭐️' + str(value)
        else:
            text1 = key[0:10] + ' ⭐️' + str(value)
        buttons.append(InlineKeyboardButton(
            text = text1,
            callback_data= ReviewCallbackFactory(
                review = key,
                grade = value
            ).pack()
        )
        )
    data = 'th:'+ str(th_id) + ':'+str(th_name)
    buttons.append(InlineKeyboardButton(text='Информация об учителе', callback_data=data))
    buttons.append(InlineKeyboardButton(text='<<', callback_data='backward_review'))
    kb_builder.row(*buttons, width=width)
    kb_builder.add(InlineKeyboardButton(text = f'{page}/{max}', callback_data='but_cl_menu'),InlineKeyboardButton(text='>>', callback_data='forward_review'))
    return kb_builder.as_markup()


def create_buttons_teachers(width: int, teachers, id):
    diction = {key: value for key, value in teachers}
    post_id = use_database.post_information.get_now_post(id)
    max = use_database.post_information.get_teacher_max_page(post_id)
    page = use_database.post_information.get_teacher_page(post_id)
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for key, value in diction.items():
        buttons.append(InlineKeyboardButton(
            text = value,
            callback_data= TeacherCallbackFactory(
                teacher_id=  key,
                teacher_name= value
            ).pack()
        )
        )
    buttons.append(InlineKeyboardButton(text='Мои заявки', callback_data='but_7'))
    buttons.append(InlineKeyboardButton(text='<<', callback_data='backward_teacher'))
    kb_builder.row(*buttons, width=width)
    kb_builder.add(InlineKeyboardButton(text = f'{page}/{max}', callback_data='but_cl_menu'),InlineKeyboardButton(text='>>', callback_data='forward_teacher'))
    return kb_builder.as_markup()

def create_buttons_posts(width: int, posts, type, id):
    diction = {key: value for key, value in posts}
    page = use_database.post_information.get_post_page(id,type)
    max = use_database.post_information.get_post_max_page(id,type)
    if (type == 'self'):
        data = 'but_cl_menu'
        forward = 'forward_self'
        backward = 'backward_self'
    elif (type == 'all'):
        data = "but_th_menu"
        forward = 'forward_all'
        backward = 'backward_all'
    elif (type == 'others'):
        data = "but_th_menu"
        forward = 'forward_others'
        backward = 'backward_others'
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for key, value in diction.items():
        if(type == 'self'):
            if(use_database.post_information.check_post_teacher_deal(key,id) is None or use_database.post_information.check_post_teacher_deal(key,id) == "None"):
                value = value + ' 🕠'
            else:
                value = value + ' ✅'
        buttons.append(InlineKeyboardButton(
            text = value,
            callback_data= PostsCallbackFactory(
                post_id = key,
                post_theme= value
            ).pack()
        )
        )
    if (type == "all"):
        buttons.append(InlineKeyboardButton(text='🕠🕠🕠 Заявки с ожиданием', callback_data='but_21'))
    buttons.append(InlineKeyboardButton(text='<<', callback_data=backward))
    kb_builder.row(*buttons, width=width)
    kb_builder.add(InlineKeyboardButton(text = f'{page}/{max}', callback_data=data),InlineKeyboardButton(text='>>', callback_data=forward))
    return kb_builder.as_markup()
