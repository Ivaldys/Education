import sqlite3
import post_information
def teacher_name(tg_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT teacher_name FROM teacher WHERE teacher_tg_id = {tg_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def teachers_surname(tg_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT teacher_surname FROM teacher WHERE teacher_tg_id = {tg_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def teachers_course(tg_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT teacher_course FROM teacher WHERE teacher_tg_id = {tg_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def teachers_phone(tg_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT teacher_phonenumber FROM teacher WHERE teacher_tg_id = {tg_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def teachers_mail(tg_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT teacher_mail FROM teacher WHERE teacher_tg_id = {tg_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def teachers_university(tg_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT teacher_university FROM teacher WHERE teacher_tg_id = {tg_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def teachers_faculty(tg_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT teacher_faculty FROM teacher WHERE teacher_tg_id = {tg_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def teachers_money(tg_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT money FROM teacher WHERE teacher_tg_id = {tg_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def teachers_id(tg_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT teacher_id FROM teacher WHERE teacher_tg_id = {tg_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def teacher_tg_id(id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT teacher_tg_id FROM teacher WHERE teacher_id = {id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def teacher_usrname(id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT teacher_username FROM teacher WHERE teacher_id = {id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def get_review_dict(user_id):
    th_id = post_information.get_teacher_page_review(user_id)
    page = post_information.get_page_review(user_id,th_id)
    new = page * 10
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT review, grade FROM deal WHERE teacher_id = {th_id} LIMIT 10 OFFSET {new}")
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result

def get_review_desc(user_id,chast, grade):
    th_id = post_information.get_teacher_page_review(user_id)
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT review FROM deal WHERE teacher_id = {th_id} AND grade = {grade}")
    result = cursor.fetchall()[0]
    connection.commit()
    connection.close()
    for i in result:
        if (chast in i):
            return i

def get_review_date(user_id, desc, grade):
    th_id = post_information.get_teacher_page_review(user_id)
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT date FROM deal WHERE teacher_id = {th_id} AND grade = {grade} AND review = '{desc}'")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def get_review_teacher(post):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT teacher_id FROM deal WHERE post_id = {post}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def set_review_desc(post,th_id, text):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE deal SET review = '{text}' WHERE post_id = {post} AND teacher_id = {th_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def set_revies_grade(post,th_id, text):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE deal SET grade = {text} WHERE post_id = {post} AND teacher_id = {th_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result