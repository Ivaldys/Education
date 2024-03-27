import sqlite3

def clients_name(tg_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT client_name FROM client WHERE client_tg_id = {tg_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def clients_surname(tg_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT client_surname FROM client WHERE client_tg_id = {tg_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def clients_course(tg_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT client_course FROM client WHERE client_tg_id = {tg_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def clients_phone(tg_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT client_phonenumber FROM client WHERE client_tg_id = {tg_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result


def clients_mail(tg_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT client_mail FROM client WHERE client_tg_id = {tg_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def clients_university(tg_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT client_university FROM client WHERE client_tg_id = {tg_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def clients_faculty(tg_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT client_faculty FROM client WHERE client_tg_id = {tg_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def clients_tg_id(id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT client_tg_id FROM client WHERE client_id = {id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def clients_username(id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT client_username FROM client WHERE client_tg_id = {id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result