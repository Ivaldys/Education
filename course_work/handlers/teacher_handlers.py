from aiogram import  Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.types import ( CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage, Redis
from config_data.config import load_config
from keyboards.user_keyboards import create_inline_kb, create_buttons_posts, PostsCallbackFactory, create_buttons_teachers
import lexiconn.lexicon_ru
import use_database.using_database
import use_database.teacher_information
import use_database.client_information
import use_database.post_information
import sqlite3

# Инициализируем роутер уровня модуля
router = Router()
config = load_config()

bot = Bot(token=config.tg_bot.token)

redis = Redis(host='localhost')

storage = RedisStorage(redis=redis)

user_dict: dict[int, dict[str, str | int | bool]] = {}

class FSMFillForm(StatesGroup):
    teacher_login  = State()
    th_edit_name = State()
    th_edit_surname = State()
    th_edit_course = State()
    th_edit_phone = State()
    th_edit_mail = State()


@router.callback_query(F.data == 'but_th_menu',  StateFilter(FSMFillForm.teacher_login))
async def teacher_login_main_menu(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    keyboard = create_inline_kb(1, 'but_5','but_18','but_8')
    await bot.send_photo(callback.message.chat.id, lexiconn.lexicon_ru.teacher_photo_url, caption = lexiconn.lexicon_ru.th_login_text(use_database.teacher_information.teacher_name(str(user_id))), reply_markup=keyboard)

#--------------------------------------------------Часть с профилем-------------------------
@router.callback_query(F.data == 'but_5',  StateFilter(FSMFillForm.teacher_login))
async def teacher_profile(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    keyboard = create_inline_kb(1, 'but_9','but_19', 'but_20', 'but_th_menu')
    user_id = callback.from_user.id
    username = 'Ваш логин тг: ' + callback.from_user.username + '\n'
    name = "Ваше имя: " + str(use_database.teacher_information.teacher_name(user_id)) + '\n'
    surname = 'Ваша фамилия: ' + str(use_database.teacher_information.teachers_surname(user_id)) + '\n'
    course ='Ваш курс: ' + str(use_database.teacher_information.teachers_course(user_id)) + '\n'
    phone ='Ваш номер: ' + str(use_database.teacher_information.teachers_phone(user_id)) + '\n'
    mail ='Ваша почта: ' + str(use_database.teacher_information.teachers_mail(user_id)) + '\n'
    unik ='Ваш университет: ' + str(use_database.teacher_information.teachers_university(user_id)) + '\n'
    faculty ='Ваш факультет: ' +  str(use_database.teacher_information.teachers_faculty(user_id)) + '\n'
    money = 'Ваш баланс:' + str(use_database.teacher_information.teachers_money(user_id)) + ' Откликов \n'
    result = '              Ваш профиль:         \n' + username + name + surname + course + phone + mail + unik + faculty
    await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)

@router.callback_query(F.data == 'but_9',  StateFilter(FSMFillForm.teacher_login))
async def teacher_profile_edit(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    keyboard = create_inline_kb(1, 'but_10','but_11', 'but_12','but_13','but_14','but_5')
    await bot.send_message(callback.message.chat.id, 'Изменить:', reply_markup= keyboard)
#--------------------------------------Изменить имя-------------------------
@router.callback_query(F.data == 'but_10',  StateFilter(FSMFillForm.teacher_login))
async def teachers_name_edit(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    name = "Ваше имя: " + str(use_database.teacher_information.teacher_name(user_id)) + '\n'
    result = '          Изменить имя         \n' + name  + '\n\n Введите пожалуйста новое имя'
    await state.set_state(FSMFillForm.th_edit_name)
    await bot.send_message(callback.message.chat.id, result)

@router.message(StateFilter(FSMFillForm.th_edit_name))
async def edit_teacher_name(message: Message, state: FSMContext):
    use_database.using_database.fill_teachers_name(message.from_user.id, message.text)
    keyboard = create_inline_kb(1,'but_5')
    await state.set_state(FSMFillForm.teacher_login)
    await bot.send_message(message.chat.id, 'Отлично, ваше имя было изменено', reply_markup= keyboard)

#--------------------------------------Изменить фамилию-------------------------
@router.callback_query(F.data == 'but_11',  StateFilter(FSMFillForm.teacher_login))
async def teacher_surname_edit(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    surname = 'Ваша фамилия: ' + str(use_database.teacher_information.teachers_surname(user_id)) + '\n'
    result = '          Изменить фамилию         \n' + surname  + '\n\n Введите пожалуйста новую фамилию'
    await state.set_state(FSMFillForm.th_edit_surnamee)
    await bot.send_message(callback.message.chat.id, result)

@router.message(StateFilter(FSMFillForm.th_edit_surnamee))
async def edit_teacher_surname(message: Message, state: FSMContext):
    use_database.using_database.fill_teachers_surname(message.from_user.id, message.text)
    keyboard = create_inline_kb(1,'but_5')
    await state.set_state(FSMFillForm.teacher_login)
    await bot.send_message(message.chat.id, 'Отлично, ваша фамилия была изменена', reply_markup= keyboard)
#--------------------------------------Изменить курс-------------------------
@router.callback_query(F.data == 'but_12',  StateFilter(FSMFillForm.teacher_login))
async def teacher_course_edit(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    course = "Ваше курс: " + str(use_database.teacher_information.teachers_course(user_id)) + '\n'
    result = '          Изменить курс         \n' + course  + '\n\n Введите пожалуйста новый курс'
    await state.set_state(FSMFillForm.th_edit_course)
    await bot.send_message(callback.message.chat.id, result)

@router.message(StateFilter(FSMFillForm.th_edit_course))
async def edit_teachert_course(message: Message, state: FSMContext):
    use_database.using_database.fill_teachers_course(message.from_user.id, message.text)
    keyboard = create_inline_kb(1,'but_5')
    await state.set_state(FSMFillForm.teacher_login)
    await bot.send_message(message.chat.id, 'Отлично, ваш курс был изменен', reply_markup= keyboard)
#--------------------------------------Изменить номер телефона-------------------------
@router.callback_query(F.data == 'but_13',  StateFilter(FSMFillForm.teacher_login))
async def teacher_phone_edit(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    phone ='Ваш номер: ' + str(use_database.teacher_information.teachers_phone(user_id)) + '\n'
    result = '          Изменить номер         \n' + phone  + '\n\n Введите пожалуйста новый номер'
    await state.set_state(FSMFillForm.th_edit_phone)
    await bot.send_message(callback.message.chat.id, result)

@router.message(StateFilter(FSMFillForm.th_edit_phone))
async def edit_teacher_phone(message: Message, state: FSMContext):
    use_database.using_database.fill_teachers_phone(message.from_user.id, message.text)
    keyboard = create_inline_kb(1,'but_5')
    await state.set_state(FSMFillForm.teacher_login)
    await bot.send_message(message.chat.id, 'Отлично, ваш номер телефона был изменен', reply_markup= keyboard)
#--------------------------------------Изменить почту-------------------------
@router.callback_query(F.data == 'but_14',  StateFilter(FSMFillForm.teacher_login))
async def teacher_mail_edit(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    mail ='Ваша почта: ' + str(use_database.teacher_information.teachers_mail(user_id)) + '\n'
    result = '          Изменить почту         \n' + mail  + '\n\n Введите пожалуйста новую почту'
    await state.set_state(FSMFillForm.th_edit_mail)
    await bot.send_message(callback.message.chat.id, result)

@router.message(StateFilter(FSMFillForm.th_edit_mail))
async def edit_teacher_mail(message: Message, state: FSMContext):
    use_database.using_database.fill_teachers_mail(message.from_user.id, message.text)
    keyboard = create_inline_kb(1,'but_5')
    await state.set_state(FSMFillForm.teacher_login)
    await bot.send_message(message.chat.id, 'Отлично, ваша почта была изменена', reply_markup= keyboard)
#--------------------------------------Пополнить баланс-------------------------
@router.callback_query(F.data == 'but_19',  StateFilter(FSMFillForm.teacher_login))
async def teacher_money(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    mail ='Ваша баланс: ' + str(use_database.teacher_information.teachers_money(user_id)) + ' Откликов \n'
    result = '          Изменить почту         \n' + mail  + '\n\n Введите пожалуйста новую почту'
    await state.set_state(FSMFillForm.th_edit_mail)
    await bot.send_message(callback.message.chat.id, result)
#--------------------------------------Просмотреть отзывы-------------------------
@router.callback_query(F.data == 'but_20',  StateFilter(FSMFillForm.teacher_login))
async def teacher_reviews(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    post_id = use_database.post_information.get_now_post(user_id)
    use_database.post_information.set_new_teacher_page(post_id)
    teachers = use_database.post_information.get_dict_otkl(post_id)
    keyboard = create_buttons_teachers(1, teachers, user_id)
    result = "---------Вот список откликнувшихся:----------\n\n *Нажмите на номер страницы, для перехода в главное меню"
    await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)

@router.callback_query(F.data == 'backward_teacher',  StateFilter(FSMFillForm.teacher_login))
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

@router.callback_query(F.data == 'forward_teacher',  StateFilter(FSMFillForm.teacher_login))
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

#--------------------------------------Просматривать все заявки-------------------------

@router.callback_query(F.data == 'but_18',  StateFilter(FSMFillForm.teacher_login))
async def teacher_all_posts(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    use_database.post_information.set_new_post_page(user_id, 'all')
    posts_info = use_database.post_information.get_posts(user_id, "all")
    keyboard = create_buttons_posts(1, posts_info, 'all', user_id )
    result = '---------Вот список постов:----------\n\n *Нажмите на номер страницы, для перехода в главное меню'
    await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)

@router.callback_query(PostsCallbackFactory.filter(),  StateFilter(FSMFillForm.teacher_login))
async def button_post_press(callback: CallbackQuery,
                                 callback_data: PostsCallbackFactory):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    id = callback.from_user.id
    post_id = callback_data.post_id
    post_theme = callback_data.post_theme
    post_desc = str(use_database.post_information.get_posts_desc(post_id, post_theme))
    text = f"---------------{post_theme}----------------" +'\n\n'+ post_desc
    use_database.post_information.set_new_now_post(id, post_id)
    use_database.post_information.set_now_post(id,post_id)
    if (use_database.post_information.check_post_teacher(id,post_id) is None or use_database.post_information.check_post_teacher(id,post_id) == "None"):
        keyboard = create_inline_kb(1, 'but_22', 'but_18')
    else:
        if (use_database.post_information.check_post_teacher_deal(post_id,id) is None or use_database.post_information.check_post_teacher_deal(post_id,id) == "None"):
            text = text + '\n\n В ожидании🕠'
            keyboard = create_inline_kb(1, 'but_18')
        else:
            text = text + '\n\n Принято!!✅✅✅'
            keyboard = create_inline_kb(1,'but_23', 'but_18')

    await bot.send_message(callback.message.chat.id, text, reply_markup= keyboard)
    await callback.answer()

@router.callback_query(F.data == 'backward_all',  StateFilter(FSMFillForm.teacher_login))
async def back_all(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    page = use_database.post_information.get_post_page(user_id, 'all')
    if(page > 1):
        use_database.post_information.set_post_page(user_id, 'all', '<<')
        posts_info = use_database.post_information.get_posts(user_id, "all")
        keyboard = create_buttons_posts(1, posts_info, 'all', user_id )
        result = '---------Вот список постов:----------\n\n *Нажмите на номер страницы, для перехода в главное меню'
        await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)
    await callback.answer()

@router.callback_query(F.data == 'forward_all',  StateFilter(FSMFillForm.teacher_login))
async def for_all(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    page = use_database.post_information.get_post_page(user_id, 'all')
    max = use_database.post_information.get_post_max_page(user_id, 'all')
    if(page < max):
        use_database.post_information.set_post_page(user_id, 'all', '>>')
        posts_info = use_database.post_information.get_posts(user_id, "all")
        keyboard = create_buttons_posts(1, posts_info, 'all', user_id )
        result = '---------Вот список постов:----------\n\n *Нажмите на номер страницы, для перехода в главное меню'
        await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)
    await callback.answer()

#--------------------------------------Откликнуться-------------------------
@router.callback_query(F.data == 'but_22',  StateFilter(FSMFillForm.teacher_login))
async def otklick(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    post_id = use_database.post_information.get_now_post(user_id)
    try:
        use_database.post_information.set_post_teacher(user_id, post_id)
        text = 'Отклик был произведен успешно!'
    except:
        text = 'Что-то пошло не так, вероятно вы уже откликнулись на этот пост'
    keyboard = create_inline_kb(1,'but_18')
    await bot.send_message(callback.message.chat.id, text, reply_markup= keyboard)

#--------------------------------------Заявки с ожиданием-------------------------
@router.callback_query(F.data == 'but_21',  StateFilter(FSMFillForm.teacher_login))
async def teacher_otkl_posts(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    use_database.post_information.set_new_post_page(user_id, 'others')
    posts_info = use_database.post_information.get_posts(user_id, "others")
    keyboard = create_buttons_posts(1, posts_info, 'others', user_id )
    result = '---------Вот список постов:----------\n\n *Нажмите на номер страницы, для перехода в главное меню'
    await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)

@router.callback_query(F.data == 'backward_others',  StateFilter(FSMFillForm.teacher_login))
async def back_others(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    page = use_database.post_information.get_post_page(user_id, 'others')
    if(page > 1):
        use_database.post_information.set_post_page(user_id, 'others', '<<')
        posts_info = use_database.post_information.get_posts(user_id, "others")
        keyboard = create_buttons_posts(1, posts_info, 'others', user_id )
        result = '---------Вот список постов:----------\n\n *Нажмите на номер страницы, для перехода в главное меню'
        await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)
    await callback.answer()

@router.callback_query(F.data == 'forward_others',  StateFilter(FSMFillForm.teacher_login))
async def for_others(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    page = use_database.post_information.get_post_page(user_id, 'others')
    max = use_database.post_information.get_post_max_page(user_id, 'others')
    if(page < max):
        use_database.post_information.set_post_page(user_id, 'others', '>>')
        posts_info = use_database.post_information.get_posts(user_id, "others")
        keyboard = create_buttons_posts(1, posts_info, 'others', user_id )
        result = '---------Вот список постов:----------\n\n *Нажмите на номер страницы, для перехода в главное меню'
        await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)
    await callback.answer()

#--------------------------------------Открыть контакты клиента-------------------------
@router.callback_query(F.data == 'but_23',  StateFilter(FSMFillForm.teacher_login))
async def open_contacts(callback: CallbackQuery,  state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user_id = callback.from_user.id
    post_id = use_database.post_information.get_now_post(user_id)
    client_id = use_database.post_information.get_clientid_by_post(post_id)
    tg_id = use_database.client_information.clients_tg_id(client_id)
    name = "Имя: " + use_database.client_information.clients_name(tg_id) + '\n'
    surname = "Фамилия: " + str(use_database.client_information.clients_surname(tg_id)) + '\n'
    phone ='Номер клиента: ' + str(use_database.client_information.clients_phone(tg_id)) + '\n'
    mail ='Почта клиента: ' + str(use_database.client_information.clients_mail(tg_id)) + '\n\n'
    username = 'Логин телеграмм: @'  + str(use_database.client_information.clients_username(tg_id)) + '\n'
    keyboard = create_inline_kb(1,'but_18')
    result = '-------Информация о пользователе----\n'+name+surname+phone+mail+username
    await bot.send_message(callback.message.chat.id, result, reply_markup= keyboard)