import sqlite3


def check_clients_authorization(clients_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM client WHERE client_tg_id = ?", (clients_id,))
    result = cursor.fetchone()
    connection.close()
    if (result):
       return True
    else:
       return False

def check_teachers_authorization(teachers_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM teacher WHERE teacher_tg_id = ?", (teachers_id,))
    result = cursor.fetchone()
    connection.close()
    if (result):
       return True
    else:
       return False


def new_teacher(id, username):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO teacher (teacher_username, teacher_tg_id, teacher_name, teacher_surname, teacher_course, teacher_phonenumber, money) VALUES('{str(username)}',{int(id)}, 'nothing', 'nothing', 0, 'nothing', 10 )")
    connection.commit()
    connection.close()

def fill_teachers_name(id, name):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE teacher SET teacher_name = '{name}' WHERE teacher_tg_id = {id}")
    connection.commit()
    connection.close()

def fill_teachers_surname(id, surname):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE teacher SET teacher_surname = '{surname}' WHERE teacher_tg_id = {id}")
    connection.commit()
    connection.close()

def fill_teachers_course(id, course):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE teacher SET teacher_course = {int(course)} WHERE teacher_tg_id = {id}")
    connection.commit()
    connection.close()

def fill_teachers_phone(id, phone):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE teacher SET teacher_phonenumber = '{phone}' WHERE teacher_tg_id = {id}")
    connection.commit()
    connection.close()

def fill_teachers_mail(id, mail):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE teacher SET teacher_mail = '{mail}' WHERE teacher_tg_id = {id}")
    connection.commit()
    connection.close()

def fill_teachers_university(id, uni):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    result = " "
    if uni == 'but_3':
        result = "НИУ ВШЭ"
    cursor.execute(f"UPDATE teacher SET teacher_university = '{result}' WHERE teacher_tg_id = {id}")
    connection.commit()
    connection.close()

def fill_teachers_faculty(id, fac):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    result = " "
    if fac == 'but_4':
        result = 'ФКН'
    cursor.execute(f"UPDATE teacher SET teacher_faculty = '{result}' WHERE teacher_tg_id = {id}")
    connection.commit()
    connection.close()

def new_client(id, username):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO client (client_username, client_tg_id, client_name, client_surname, client_course, client_phonenumber) VALUES('{str(username)}',{int(id)}, 'nothing', 'nothing', 0, 'nothing' )")
    connection.commit()
    connection.close()

def fill_clients_name(id, name):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE client SET client_name = '{name}' WHERE client_tg_id = {id}")
    connection.commit()
    connection.close()

def fill_clients_surname(id, surname):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE client SET client_surname = '{surname}' WHERE client_tg_id = {id}")
    connection.commit()
    connection.close()

def fill_clients_course(id, course):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE client SET client_course = {int(course)} WHERE client_tg_id = {id}")
    connection.commit()
    connection.close()

def fill_clients_phone(id, phone):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE client SET client_phonenumber = '{phone}' WHERE client_tg_id = {id}")
    connection.commit()
    connection.close()

def fill_clients_mail(id, mail):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE client SET client_mail = '{mail}' WHERE client_tg_id = {id}")
    connection.commit()
    connection.close()

def fill_clients_university(id, uni):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    result = " "
    if uni == 'but_3':
        result = "НИУ ВШЭ"
    cursor.execute(f"UPDATE client SET client_university = '{result}' WHERE client_tg_id = {id}")
    connection.commit()
    connection.close()

def fill_clients_faculty(id, fac):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    result = " "
    if fac == 'but_4':
        result = 'ФКН'
    cursor.execute(f"UPDATE client SET client_faculty = '{result}' WHERE client_tg_id = {id}")
    connection.commit()
    connection.close()

def get_users_page(user_id, teacher_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT page FROM page_review WHERE user_id = {user_id} and teacher_id = {teacher_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def set_users_page(user_id, teacher_id):
    id = str(user_id)+str(teacher_id)
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT OR IGNORE INTO page_review (page_review_id, user_id, teacher_id, page) VALUES ('{id}',{user_id}, {teacher_id}, 1)")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result