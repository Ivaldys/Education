from aiogram import  Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.types import ( CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage, Redis
from config_data.config import load_config
from keyboards.user_keyboards import create_inline_kb, create_buttons_posts, PostsCallbackFactory, create_buttons_teachers, TeacherCallbackFactory, create_buttons_reviews, ReviewCallbackFactory
import lexiconn.lexicon_ru
import use_database.using_database
import use_database.client_information
import use_database.post_information
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
    cl_edit_name = State()
    cl_edit_surname = State()
    cl_edit_course = State()
    cl_edit_phone = State()
    cl_edit_mail = State()
    cl_post_theme = State()
    cl_post_desc = State()
    cl_post_cost = State()
    cl_rev_desc = State()
    cl_rev_grade = State()
    teacher_login  = State()

@router.callback_query(F.data == 'but_cl_menu',  StateFilter(FSMFillForm.client_login))
async def client_main_menu(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    keyboard = create_inline_kb(1, 'but_5','but_6','but_7','but_8')
    await bot.send_photo(callback.message.chat.id, lexiconn.lexicon_ru.client_photo_url, caption = lexiconn.lexicon_ru.cl_login_text(use_database.client_information.clients_name(str(user_id))), reply_markup=keyboard)

#------------------------------------------------Часть с профилем и его изменением--------------------------------
@router.callback_query(F.data == 'but_5',  StateFilter(FSMFillForm.client_login))
async def client_profile(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    keyboard = create_inline_kb(1, 'but_9', 'but_cl_menu')
    user_id = callback.from_user.id
    username = 'Ваш логин тг: ' + callback.from_user.username + '\n'
    name = "Ваше имя: " + str(use_database.client_information.clients_name(user_id)) + '\n'
    surname = 'Ваша фамилия: ' + str(use_database.client_information.clients_surname(user_id)) + '\n'
    course ='Ваш курс: ' + str(use_database.client_information.clients_course(user_id)) + '\n'
    phone ='Ваш номер: ' + str(use_database.client_information.clients_phone(user_id)) + '\n'
    mail ='Ваша почта: ' + str(use_database.client_information.clients_mail(user_id)) + '\n'
    unik ='Ваш университет: ' + str(use_database.client_information.clients_university(user_id)) + '\n'
    faculty ='Ваш факультет: ' +  str(use_database.client_information.clients_faculty(user_id)) + '\n'
    result = '              Ваш профиль:         \n' + username + name + surname + course + phone + mail + unik + faculty
    await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)

@router.callback_query(F.data == 'but_9',  StateFilter(FSMFillForm.client_login))
async def client_profile_edit(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    keyboard = create_inline_kb(1, 'but_10','but_11', 'but_12','but_13','but_14','but_5')
    await bot.send_message(callback.message.chat.id, 'Изменить:', reply_markup= keyboard)

@router.callback_query(F.data == 'but_10',  StateFilter(FSMFillForm.client_login))
async def client_name_edit(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    name = "Ваше имя: " + str(use_database.client_information.clients_name(user_id)) + '\n'
    result = '          Изменить имя         \n' + name  + '\n\n Введите пожалуйста новое имя'
    await state.set_state(FSMFillForm.cl_edit_name)
    await bot.send_message(callback.message.chat.id, result)

@router.message(StateFilter(FSMFillForm.cl_edit_name))
async def edit_client_name(message: Message, state: FSMContext):
    use_database.using_database.fill_clients_name(message.from_user.id, message.text)
    keyboard = create_inline_kb(1,'but_5')
    await state.set_state(FSMFillForm.client_login)
    await bot.send_message(message.chat.id, 'Отлично, ваше имя было изменено', reply_markup= keyboard)

@router.callback_query(F.data == 'but_11',  StateFilter(FSMFillForm.client_login))
async def client_surname_edit(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    surname = 'Ваша фамилия: ' + str(use_database.client_information.clients_surname(user_id)) + '\n'
    result = '          Изменить фамилию         \n' + surname  + '\n\n Введите пожалуйста новую фамилию'
    await state.set_state(FSMFillForm.cl_edit_surname)
    await bot.send_message(callback.message.chat.id, result)

@router.message(StateFilter(FSMFillForm.cl_edit_surname))
async def edit_client_surname(message: Message, state: FSMContext):
    use_database.using_database.fill_clients_surname(message.from_user.id, message.text)
    keyboard = create_inline_kb(1,'but_5')
    await state.set_state(FSMFillForm.client_login)
    await bot.send_message(message.chat.id, 'Отлично, ваша фамилия была изменена', reply_markup= keyboard)

@router.callback_query(F.data == 'but_12',  StateFilter(FSMFillForm.client_login))
async def client_course_edit(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    course = "Ваше курс: " + str(use_database.client_information.clients_course(user_id)) + '\n'
    result = '          Изменить курс         \n' + course  + '\n\n Введите пожалуйста новый курс'
    await state.set_state(FSMFillForm.cl_edit_course)
    await bot.send_message(callback.message.chat.id, result)
####################################
@router.message(StateFilter(FSMFillForm.cl_edit_course))
async def edit_client_course(message: Message, state: FSMContext):
    use_database.using_database.fill_clients_course(message.from_user.id, message.text)
    keyboard = create_inline_kb(1,'but_5')
    await state.set_state(FSMFillForm.client_login)
    await bot.send_message(message.chat.id, 'Отлично, ваш курс был изменен', reply_markup= keyboard)

@router.callback_query(F.data == 'but_13',  StateFilter(FSMFillForm.client_login))
async def client_phone_edit(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    phone ='Ваш номер: ' + str(use_database.client_information.clients_phone(user_id)) + '\n'
    result = '          Изменить номер         \n' + phone  + '\n\n Введите пожалуйста новый номер'
    await state.set_state(FSMFillForm.cl_edit_phone)
    await bot.send_message(callback.message.chat.id, result)

@router.message(StateFilter(FSMFillForm.cl_edit_phone))
async def edit_client_phone(message: Message, state: FSMContext):
    use_database.using_database.fill_clients_phone(message.from_user.id, message.text)
    keyboard = create_inline_kb(1,'but_5')
    await state.set_state(FSMFillForm.client_login)
    await bot.send_message(message.chat.id, 'Отлично, ваш номер телефона был изменен', reply_markup= keyboard)
##########
@router.callback_query(F.data == 'but_14',  StateFilter(FSMFillForm.client_login))
async def client_mail_edit(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    mail ='Ваша почта: ' + str(use_database.client_information.clients_mail(user_id)) + '\n'
    result = '          Изменить почту         \n' + mail  + '\n\n Введите пожалуйста новую почту'
    await state.set_state(FSMFillForm.cl_edit_mail)
    await bot.send_message(callback.message.chat.id, result)

@router.message(StateFilter(FSMFillForm.cl_edit_mail))
async def edit_client_mail(message: Message, state: FSMContext):
    use_database.using_database.fill_clients_mail(message.from_user.id, message.text)
    keyboard = create_inline_kb(1,'but_5')
    await state.set_state(FSMFillForm.client_login)
    await bot.send_message(message.chat.id, 'Отлично, ваша почта была изменена', reply_markup= keyboard)
#------------------------------------------------Часть с созданием новой заявки--------------------------------

@router.callback_query(F.data == 'but_6',  StateFilter(FSMFillForm.client_login))
async def client_new_post(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    result = '---------СОЗДАТЬ ПОСТ----------\nТут вы можете создать ваш пост (Состоящий из темы поста, описания и стоимости в рублях), для этого нажмите на кнопку и мы начнем'
    keyboard = create_inline_kb(1,'but_15', 'but_cl_menu')
    await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)

@router.callback_query(F.data == 'but_15',  StateFilter(FSMFillForm.client_login))
async def client_generate_new_post(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    result = 'Отлично! Введите пожалуйста тему вашего поста!'
    await bot.send_message(callback.message.chat.id, result)
    await state.set_state(FSMFillForm.cl_post_theme)

@router.message(StateFilter(FSMFillForm.cl_post_theme))
async def new_post_generated(message: Message, state: FSMContext):
    use_database.post_information.new_post(message.from_user.id, message.text, message.date)
    result = 'Далее, введите пожалуйста подробное описание вашего поста'
    await bot.send_message(message.chat.id, result)
    await state.set_state(FSMFillForm.cl_post_desc)

@router.message(StateFilter(FSMFillForm.cl_post_desc))
async def generate_post_desc(message: Message, state: FSMContext):
    use_database.post_information.fill_post_desc(message.from_user.id, message.text)
    result = 'Далее, введите пожалуйста цену за урок! (Целое число)'
    await bot.send_message(message.chat.id, result)
    await state.set_state(FSMFillForm.cl_post_cost)

@router.message(StateFilter(FSMFillForm.cl_post_cost))
async def generate_post_cost(message: Message, state: FSMContext):
    try:
        use_database.post_information.fill_post_cost(message.from_user.id, message.text)
        result = 'Поздравляем! Пост был создан!'
        keyboard = create_inline_kb(1, 'but_cl_menu')
        await bot.send_message(message.chat.id, result, reply_markup = keyboard)
        await state.set_state(FSMFillForm.client_login)
    except Exception:
        result = 'Введите пожалуйста ЧИСЛО'
        await bot.send_message(message.chat.id, result)

#------------------------------------------------Часть с просмотром своих заявок--------------------------------

@router.callback_query(F.data == 'but_7',  StateFilter(FSMFillForm.client_login))
async def clients_post(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    use_database.post_information.set_new_post_page(user_id,'self')
    posts_info = use_database.post_information.get_posts(callback.from_user.id, "self")
    keyboard = create_buttons_posts(1, posts_info, 'self', callback.from_user.id )
    result = '---------Вот список ваших постов:----------\n\n *Нажмите на номер страницы, для перехода в главное меню'
    await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)

@router.callback_query(F.data == 'backward_self',  StateFilter(FSMFillForm.client_login))
async def back_self(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    page = use_database.post_information.get_post_page(user_id, 'self')
    if(page > 1):
        use_database.post_information.set_post_page(user_id, 'self', '<<')
        posts_info = use_database.post_information.get_posts(user_id, "self")
        keyboard = create_buttons_posts(1, posts_info, 'self', user_id )
        result = '---------Вот список ваших постов:----------\n\n *Нажмите на номер страницы, для перехода в главное меню'
        await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)
    await callback.answer()

@router.callback_query(F.data == 'forward_self',  StateFilter(FSMFillForm.client_login))
async def for_self(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    page = use_database.post_information.get_post_page(user_id, 'self')
    max = use_database.post_information.get_post_max_page(user_id, 'self')
    if(page < max):
        use_database.post_information.set_post_page(user_id, 'self', '>>')
        posts_info = use_database.post_information.get_posts(user_id, "self")
        keyboard = create_buttons_posts(1, posts_info, 'self', user_id )
        result = '---------Вот список ваших постов:----------\n\n *Нажмите на номер страницы, для перехода в главное меню'
        await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)
    await callback.answer()
#------------------------------------------------Часть с просмотром инфы о заявке--------------------------------
@router.callback_query(PostsCallbackFactory.filter(),  StateFilter(FSMFillForm.client_login))
async def process_category_press(callback: CallbackQuery,
                                 callback_data: PostsCallbackFactory):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    id = callback.from_user.id
    post_id = callback_data.post_id
    post_theme = callback_data.post_theme
    post_desc = str(use_database.post_information.get_posts_desc(post_id, post_theme))
    text = f"---------------{post_theme}----------------" +'\n\n'+ post_desc
    use_database.post_information.set_new_now_post(id, post_id)
    use_database.post_information.set_now_post(id,post_id)
    keyboard = create_inline_kb(1, 'but_7', 'but_17')
    await bot.send_message(callback.message.chat.id, text, reply_markup= keyboard)
    await callback.answer()
#------------------------------------------------Часть с просмотром откликнувшихся--------------------------------
@router.callback_query(F.data == 'but_17',  StateFilter(FSMFillForm.client_login))
async def spisok_otkl(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    post_id = use_database.post_information.get_now_post(user_id)
    use_database.post_information.set_new_teacher_page(post_id)
    teachers = use_database.post_information.get_dict_otkl(post_id)
    keyboard = create_buttons_teachers(1, teachers, user_id)
    result = "---------Вот список откликнувшихся:----------\n\n *Нажмите на номер страницы, для перехода в главное меню"
    await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)

@router.callback_query(F.data == 'backward_teacher',  StateFilter(FSMFillForm.client_login))
async def back_teacher(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    post = use_database.post_information.get_now_post(user_id)
    page = use_database.post_information.get_teacher_page(post)
    if(page > 1):
        use_database.post_information.set_teacher_page(post, '<<')
        teachers = use_database.post_information.get_dict_otkl(post)
        keyboard = create_buttons_teachers(1, teachers, user_id)
        result = "---------Вот список откликнувшихся:----------\n\n *Нажмите на номер страницы, для перехода в главное меню"
        await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)
    await callback.answer()

@router.callback_query(F.data == 'forward_teacher',  StateFilter(FSMFillForm.client_login))
async def for_teacher(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    post = use_database.post_information.get_now_post(user_id)
    page = use_database.post_information.get_teacher_page(post)
    max = use_database.post_information.get_teacher_max_page(post)
    if(page < max):
        use_database.post_information.set_teacher_page(post, '>>')
        teachers = use_database.post_information.get_dict_otkl(post)
        keyboard = create_buttons_teachers(1, teachers, user_id)
        result = "---------Вот список откликнувшихся:----------\n\n *Нажмите на номер страницы, для перехода в главное меню"
        await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)
    await callback.answer()

#------------------------------------------------Часть с просмотром инфы о пользователе--------------------------------
@router.callback_query(TeacherCallbackFactory.filter(),  StateFilter(FSMFillForm.client_login))
async def button_teacher_info_press(callback: CallbackQuery,
                                 callback_data: TeacherCallbackFactory):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    post_id = use_database.post_information.get_now_post(user_id)
    th_id = callback_data.teacher_id
    th_name = "Имя: " + str(callback_data.teacher_name) + '\n'
    tg_id = use_database.teacher_information.teacher_tg_id(th_id)
    th_surname = "Фамилия: " + str(use_database.teacher_information.teachers_surname(tg_id)) + "\n"
    th_course = "Курс: " + str(use_database.teacher_information.teachers_course(tg_id)) + "\n"
    th_faculty ="Факультет: " + str(use_database.teacher_information.teachers_faculty(tg_id)) + "\n"
    th_unik = "Универ: " + str(use_database.teacher_information.teachers_university(tg_id)) + "\n"
    th_phone = "Номер телефона: " + str(use_database.teacher_information.teachers_phone(tg_id)) + "\n"
    th_mail = "Почта: " + str(use_database.teacher_information.teachers_mail(tg_id)) + "\n"
    th_username = "Логин телеграмм: @" + use_database.teacher_information.teacher_usrname(th_id) + "\n"
    text = f"---------------{th_name} {th_surname}----------------" +'\n\n'+ th_unik + th_faculty + th_course
    use_database.post_information.set_new_page_review(callback.from_user.id, th_id)
    use_database.post_information.set_page_review(callback.from_user.id, th_id, '.')
    post_check = use_database.teacher_information.get_review_teacher(post_id)
    if(post_check == 0):
        keyboard = create_inline_kb(1, 'but_25', 'but_24')
        text = f"---------------{th_name} {th_surname}----------------" +'\n\n'+ th_unik + th_faculty + th_course
    else:
        keyboard = create_inline_kb(1, 'but_25')
        text = f"---------------{th_name} {th_surname}----------------" +'\n\n'+ th_unik + th_faculty + th_course + '\n\nПохоже, что вы уже приняли отклик на эту заявку'
    await bot.send_message(callback.message.chat.id, text, reply_markup= keyboard)
    await callback.answer()
#------------------------------------------------Часть с отзывами--------------------------------

@router.callback_query(F.data == 'but_25',  StateFilter(FSMFillForm.client_login))
async def spisok_otkl(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    reviews = use_database.teacher_information.get_review_dict(user_id)
    keyboard = create_buttons_reviews(1,reviews,user_id)
    result = "---------Вот список отзывов:----------\n\n *Нажмите на номер страницы, для перехода в главное меню"
    await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)

@router.callback_query(F.data == 'backward_review',  StateFilter(FSMFillForm.client_login))
async def back_review(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    th_id = use_database.post_information.get_teacher_page_review(user_id)
    page = use_database.post_information.get_page_review(user_id)
    if(page > 1):
        use_database.post_information.set_teacher_page(user_id, th_id, '<<')
        reviews = use_database.teacher_information.get_review_dict(user_id)
        keyboard = create_buttons_reviews(1,reviews,user_id)
        result = "---------Вот список отзывов:----------\n\n *Нажмите на номер страницы, для перехода в главное меню"
        await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)
    await callback.answer()

@router.callback_query(F.data == 'forward_review',  StateFilter(FSMFillForm.client_login))
async def for_review(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    th_id = use_database.post_information.get_teacher_page_review(user_id)
    page = use_database.post_information.get_page_review(user_id)
    max = use_database.post_information.get_max_page_review(user_id)
    if(page < max):
        use_database.post_information.set_teacher_page(user_id, th_id, '>>')
        reviews = use_database.teacher_information.get_review_dict(user_id)
        keyboard = create_buttons_reviews(1,reviews,user_id)
        result = "---------Вот список отзывов:----------\n\n *Нажмите на номер страницы, для перехода в главное меню"
        await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)
    await callback.answer()

#------------------------------------------------Просмотр отзыва--------------------------------
@router.callback_query(ReviewCallbackFactory.filter(),  StateFilter(FSMFillForm.client_login))
async def button_review_info_press(callback: CallbackQuery,
                                 callback_data: ReviewCallbackFactory):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    th_review_data = callback_data.review
    th_review_grade = callback_data.grade
    th_desc = use_database.teacher_information.get_review_desc(callback.from_user.id, th_desc, th_review_grade)
    th_date = 'Дата: ' + use_database.teacher_information.get_review_date(callback.from_user.id, th_desc, th_review_grade)
    text = f"---------------{th_review_data} ⭐️{th_review_grade}----------------" +'\n\n'+ th_desc + '\n\n' + th_date
    keyboard = create_inline_kb(1, 'but_25', 'but_cl_menu')
    await bot.send_message(callback.message.chat.id, text, reply_markup= keyboard)
    await callback.answer()

#------------------------------------------------Принять отклик--------------------------------

@router.callback_query(F.data == 'but_24',  StateFilter(FSMFillForm.client_login))
async def accept_otkl(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    th_id = use_database.post_information.get_teacher_page_review(user_id)
    tg_id = use_database.teacher_information.teacher_tg_id(th_id)
    th_name = "Имя: " + str(use_database.teacher_information.teacher_name(tg_id)) + '\n'
    th_surname = "Фамилия: " + str(use_database.teacher_information.teachers_surname(tg_id)) + "\n"
    th_course = "Курс: " + str(use_database.teacher_information.teachers_course(tg_id)) + "\n"
    th_faculty ="Факультет: " + str(use_database.teacher_information.teachers_faculty(tg_id)) + "\n"
    th_unik = "Универ: " + str(use_database.teacher_information.teachers_university(tg_id)) + "\n"
    th_phone = "Номер телефона: " + str(use_database.teacher_information.teachers_phone(tg_id)) + "\n"
    th_mail = "Почта: " + str(use_database.teacher_information.teachers_mail(tg_id)) + "\n"
    th_username = "Логин телеграмм: @" + use_database.teacher_information.teacher_usrname(th_id) + "\n"
    text = f"---------------{th_name} {th_surname}----------------" +'\n\n'+ th_unik + th_faculty + th_course + th_phone + th_mail + th_username + '\n\nВы можете отменить отклик, однако вам нужно подтверждение преподавателя'
    keyboard = create_inline_kb(1, 'but_27', 'but_28', 'but_17')
    await bot.send_message(callback.message.chat.id, text, reply_markup= keyboard)
#------------------------------------------------Оставить отзыв--------------------------------
@router.callback_query(F.data == 'but_27',  StateFilter(FSMFillForm.client_login))
async def set_rev(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    text = 'Отправьте пожалуйста сообщение с вашим отзывом о выполненном заказе'
    await bot.send_message(callback.message.chat.id, text)
    await state.set_state(FSMFillForm.cl_rev_desc)

@router.message(StateFilter(FSMFillForm.cl_rev_desc))
async def set_text_rev(message: Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id
    post = use_database.post_information.get_now_post(user_id)
    th_id = use_database.post_information.get_teacher_page_review(user_id)
    use_database.teacher_information.set_review_desc(post,th_id, text)
    text = 'Отзыв сохранен, оцените работу преподавателя от 1 до 5\n\nОтправьте соответствующую цифру'
    await bot.send_message(message.chat.id, text)
    await state.set_state(FSMFillForm.cl_rev_grade)


@router.message(StateFilter(FSMFillForm.cl_rev_grade))
async def set_grade_rev(message: Message, state: FSMContext):
    text = message.text
    gr = 0
    try:
        gr = int(text)
        user_id = message.from_user.id
        post = use_database.post_information.get_now_post(user_id)
        th_id = use_database.post_information.get_teacher_page_review(user_id)
        use_database.teacher_information.set_revies_grade(post,th_id, text)
        text = 'Ваша оценка учтена!'
        keyboard = create_inline_kb(1,'but_cl_menu')
        await state.set_state(FSMFillForm.client_login)
        await bot.send_message(message.chat.id, text, reply_markup= keyboard)
    except:
        await bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте еще раз (Отправьте число от 1 до 5)')

#--------------------------------------------------------------------------------
@router.callback_query(F.data == 'but_28',  StateFilter(FSMFillForm.client_login))
async def del_deal(callback: CallbackQuery,  state: FSMContext):
