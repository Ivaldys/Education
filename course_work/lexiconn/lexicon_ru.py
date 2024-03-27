LEXICON_COMMANDS_RU: dict[str, str] = {
    '/start': 'Вернуться к началу',
    '/description': 'Описание работы бота',
    '/contact': 'контакты создателя',
    '/help': 'Помощь по работе бота'
}

lexicon_start = 'Приветствую, я - телеграмм бот, который поможет вам найти хорошего репетитора по нужному предмету или стать им!💫🙋‍♂️ \n\n\n     *__ТИП АВТОРИЗАЦИИ:__*'

def cl_login_text(name):
    lexicon_cl_login = f'                            Добро пожаловать,{name}!!!                             ' + '\n'
    lexicon_text = lexicon_cl_login + 'Вы авторизованы в качестве ученика\n\n\nВам доступно:       '
    return lexicon_text

def th_login_text(name):
    lexicon_th_login = f'                            Добро пожаловать,{name}!!!                             ' + '\n'
    lexicon_text = lexicon_th_login + 'Вы авторизованы в качестве репетитора!\n\n\nВам доступно:       '
    return lexicon_text

BUTTONS: dict[str, str] = {
    'but_1': 'Ученик 🤓',
    'but_cl_menu': 'Главное меню 🤓',
    'but_th_menu': 'Главное меню 😉',
    'but_2': 'Репетитор 😉',
    'but_3': 'НИУ ВШЭ',
    'but_4': 'ФКН',
    'but_5': 'МОЙ ПРОФИЛЬ',
    'but_6': 'НОВАЯ ЗАЯВКА',
    'but_7': 'МОИ ЗАЯВКИ',
    'but_8': 'Выход ❌❌❌',
    'but_9': 'Изменить',
    'but_10': 'ИМЯ',
    'but_11': 'Фамилия',
    'but_12': 'Курс',
    'but_13': 'Номер телефона',
    'but_14': 'Почта',
    'but_15': 'Создать заявку🆕🆕🆕',
    'but_17': 'Откликнувшиеся',
    'but_18': 'Смотреть заявки',
    'but_19': 'Пополнить баланс',
    'but_20': 'Мои отзывы',
    'but_21': 'Заявки с откликом',
    'but_22': 'Отклик',
    'but_23': 'Контакты клиента',
    'but_24': 'Принять ✅✅✅',
    'but_25': 'Посмотреть отзывы',
    'but_27': 'Оставить отзыв',
    'but_28': 'Отменить отклик'
    }

photo_url = 'https://sun9-79.userapi.com/impg/1_0heAt_NWUx_aK3jaTePjDFnYEI7PySy9vZtg/XUfR6sfFObs.jpg?size=736x736&quality=96&sign=d8e4add6b3c029fbeb7b3fcd51631643&type=album'

teacher_photo_url = 'https://sun9-24.userapi.com/impg/cZkgc41DiApPZRyMfBICwQ3AvZJn6CTcIY4Zeg/HR-EyEFoSkM.jpg?size=1024x1024&quality=96&sign=52e4a268ae97087942ca10e0f2f7590b&type=album'
client_photo_url = 'https://sun9-24.userapi.com/impg/zvSgjp9YxN9YM43QcxhiyblYeNxBrdFrpvPwHw/EXxPPrdGs5A.jpg?size=1170x1134&quality=96&sign=8f13347e40baab0cc71036833a830059&type=album'