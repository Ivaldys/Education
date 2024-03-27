import sqlite3

def new_post(client_id, post_theme,date):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute(f""" SELECT client_id
                        FROM client
                        WHERE client_tg_id = {client_id}
                   """)

    result = int(cursor.fetchone()[0])

    cursor.execute(f"INSERT INTO post (post_theme, post_desc, post_cost, client_id) VALUES('{post_theme}',' ', 0, {result})")
    connection.commit()

    cursor.execute(f"""INSERT INTO deal (post_id, client_id, teacher_id, date)
                       SELECT post_id, client_id, 0, '{str(date)[:10]}'
                       FROM post
                       WHERE post_theme = '{post_theme}' and client_id = {result}
                       ;
                   """)
    connection.commit()
    connection.close()

def fill_post_desc(client_id, desc):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute(f""" SELECT client_id
                        FROM client
                        WHERE client_tg_id = {client_id}
                   """)
    result = cursor.fetchone()[0]

    cursor.execute(f""" SELECT post_id
                        FROM deal
                        WHERE client_id = {result}
                        ORDER BY date DESC
                        LIMIT 1
                   """)
    identi = cursor.fetchone()[0]

    cursor.execute(f"UPDATE post SET post_desc = '{desc}' WHERE post_id = {identi}")
    connection.commit()
    connection.close()


def fill_post_cost(client_id, cost):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute(f""" SELECT client_id
                        FROM client
                        WHERE client_tg_id = {client_id}
                   """)
    result = cursor.fetchone()[0]

    cursor.execute(f""" SELECT post_id
                        FROM deal
                        WHERE client_id = {result}
                        ORDER BY date DESC
                        LIMIT 1
                   """)
    identi = cursor.fetchone()[0]

    cursor.execute(f"UPDATE post SET post_cost = '{int(cost)}' WHERE post_id = {identi}")
    connection.commit()
    connection.close()

def get_posts(id, type):
    if (type == "self"):
        page = get_post_page(id, 'self')
        client_id = get_id_fromtg(id, 'client')
        selection = page * 10
        text = f"SELECT post_id, post_theme FROM post WHERE client_id = {client_id} LIMIT 10 OFFSET {selection}"
    elif (type == "all"):
        page = get_post_page(id, 'all')
        selection = page * 10
        text = f"SELECT post_id, post_theme FROM post LIMIT 10 OFFSET {selection}"
    elif (type == "others"):
        page = get_post_page(id, 'others')
        teacher_id = get_id_fromtg(id, 'teacher')
        selection = page * 10
        text = f"SELECT post_id, post_theme FROM post INNER JOIN post_teacher ON post.post_id = post_teacher.post_id WHERE teacher_id = {teacher_id} LIMIT 10 OFFSET {selection}"
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(text)
    posts = cursor.fetchall()
    connection.commit()
    connection.close()
    return posts

def get_post_page(id, type):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f""" SELECT page
                        FROM page_post
                        WHERE id = {id} and type = '{type}'
                   """)
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def set_new_post_page(id,type):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT OR IGNORE INTO page_post(id, page, type) VALUES({id},1, '{type}')")
    connection.commit()
    connection.close()

def set_post_page(id,type, strelka):
    page = get_post_page(id,type)
    if (strelka == ">>"):
        page = page + 1
    elif (strelka == "<<"):
        page = page - 1
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE page_post SET page = {page} WHERE id = {id} AND type = '{type}'")
    connection.commit()
    connection.close()

def get_post_max_page(id, type):
    if (type == "self"):
        client_id = get_id_fromtg(id, 'client')
        text = f"SELECT COUNT(*) FROM post WHERE client_id = {client_id}"
    elif (type == "all"):
        text = f"SELECT COUNT(*) FROM post"
    elif (type == "others"):
        teacher_id = get_id_fromtg(id, 'teacher')
        text = f"SELECT COUNT(*) FROM post_teacher WHERE teacher_id = {teacher_id}"
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(text)
    result = int(cursor.fetchone()[0])
    fraction = 0
    if (result % 10 != 0):
        fraction = 1
    answer = (result // 10) + fraction
    connection.commit()
    connection.close()
    return answer

def get_id_fromtg(id, type):
    if (type == "client"):
        text = f""" SELECT client_id
                        FROM client
                        WHERE client_tg_id = {id}
                   """
    elif (type == "teacher"):
        text = f""" SELECT teacher_id
                        FROM teacher
                        WHERE teacher_tg_id = {id}
                   """
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(text)
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def get_posts_desc(id, theme):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f""" SELECT post_desc
                        FROM post
                        WHERE post_id = {id} and post_theme = '{theme}'
                   """)
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def set_new_now_post(id, post):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT OR IGNORE INTO user_post(id, post_id) VALUES({id}, {post})")
    connection.commit()
    connection.close()

def set_now_post(id, post):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE user_post SET post_id = {post} WHERE id = {id}")
    connection.commit()
    connection.close()
def get_now_post(id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT post_id FROM user_post WHERE id = {id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def set_post_teacher(id, post):
    teacher_id = get_id_fromtg(id,'teacher')
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO post_teacher(post_id, teacher_id) VALUES({post}, {teacher_id})")
    connection.commit()
    connection.close()

def check_post_teacher(id,post):
    teacher_id = get_id_fromtg(id,'teacher')
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT post_id FROM post_teacher WHERE post_id = {post} AND teacher_id = {teacher_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def check_post_teacher_deal(post_id,id):
    teacher_id = get_id_fromtg(id, 'teacher')
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT post_id FROM deal WHERE post_id = {post_id} AND teacher_id = {teacher_id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def get_clientid_by_post(post):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT client_id FROM post WHERE post_id = {post}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def get_dict_otkl(post):
    page = get_teacher_page(post)
    new = page * 10
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT teacher_id, teacher_name FROM post_teacher INNER JOIN teacher ON post_teacher.teacher_id = teacher.teacher_id WHERE post_id = {post} LIMIT 10 OFFSET {new}")
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result

def get_teacher_max_page(post):
    text = f"SELECT COUNT(*) FROM post_teacher WHERE post_id = {post}"
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(text)
    result = int(cursor.fetchone()[0])
    fraction = 0
    if (result % 10 != 0):
        fraction = 1
    answer = (result // 10) + fraction
    connection.commit()
    connection.close()
    return answer

def get_teacher_page(post):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT page FROM page_otklik WHERE post_id = {post}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def set_new_teacher_page(post):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT OR IGNORE INTO page_otklik(post_id, page) VALUES({post}, {1})")
    connection.commit()
    connection.close()

def set_teacher_page(post, strelka):
    page = get_teacher_page(post)
    if (strelka == "<<"):
        page = page - 1
    elif (strelka == ">>"):
        page = page + 1
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE page_otklik SET page = {page} WHERE post_id = {post}")
    connection.commit()
    connection.close()

def set_new_page_review(id,th_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT OR IGNORE INTO page_review(user_id, teacher_id, page) VALUES({id}, {th_id}, {1})")
    connection.commit()
    connection.close()

def set_page_review(id,th_id, strelka):
    page = get_page_review(id,th_id)
    if (strelka == "<<"):
        page = page - 1
        text = f"UPDATE page_review SET page = {page} WHERE user_id = {id} AND teacher_id = {th_id}"
    elif (strelka == ">>"):
        page = page + 1
        text = f"UPDATE page_review SET page = {page} WHERE user_id = {id} AND teacher_id = {th_id}"
    elif (strelka == '.'):
        text = f"UPDATE page_review SET page = {1}, th_id = {th_id}  WHERE user_id = {id}"
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(text)
    connection.commit()
    connection.close()

def get_page_review(id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT page FROM page_review WHERE user_id = {id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result

def get_max_page_review(id):
    th_id = get_teacher_page_review(id)
    text = f"SELECT COUNT(*) FROM deal WHERE teacher_id = {th_id}"
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(text)
    result = int(cursor.fetchone()[0])
    fraction = 0
    if (result % 10 != 0):
        fraction = 1
    answer = (result // 10) + fraction
    connection.commit()
    connection.close()
    return answer

def get_teacher_page_review(id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT teacher_id FROM page_review WHERE user_id = {id}")
    result = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return result