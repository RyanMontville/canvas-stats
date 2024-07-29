import psycopg2
from colors import color_dict, color_tuples
from username_id import username_id_dict

sql_csv = open("fixed_sql.csv", "r")

conn = psycopg2.connect(database="canvas2024", user="postgres", password="password", host="127.0.0.1", port="5432")
cur = conn.cursor()


def dump_users_ranking_pixel_count_into_db():
    user_count_dict = {}
    for line in sql_csv:
        cols = line.split(",")
        log_id = cols[0]
        username = cols[1]
        x_cord = cols[2]
        y_cord = cols[3]
        color_hex = cols[4]
        time_placed = cols[5]
        is_mod_action = cols[6]
        is_top_pixel = cols[7]
        deleted_at = cols[8]
        if len(deleted_at) < 4:
            if is_mod_action == 'f':
                if username in user_count_dict:
                    user_count_dict[username] += 1
                else:
                    user_count_dict[username] = 1
    sorted_rankings = sorted(user_count_dict.items(), key=lambda kv: kv[1], reverse=True)
    for i in range(len(sorted_rankings)):
        user_rank = i + 1
        sql = f"INSERT INTO public.users(username, ranking, total_pixels_placed) VALUES ('{sorted_rankings[i][0]}', {user_rank},{sorted_rankings[i][1]});"
        cur.execute(sql)
        print(f"{user_rank} entries recorded!")


def dump_pixels_into_db():
    for line in sql_csv:
        cols = line.split(",")
        log_id = cols[0]
        username = cols[1]
        user_id = username_id_dict[username]
        x_cord = cols[2]
        y_cord = cols[3]
        color_hex = cols[4]
        color_id = color_dict[color_hex]
        time_placed = cols[5]
        is_mod_action = cols[6]
        is_top_pixel = cols[7]

        if len(cols[8]) < 4:
            sql = f"INSERT INTO public.pixels(user_id, x_cord, y_cord, color_id, time_placed, id_mod_action, is_top) VALUES('{user_id}', {x_cord}, {y_cord}, {color_id}, '{time_placed}', '{is_mod_action}', '{is_top_pixel}');"
        else:
            deleted_at = cols[8]
            sql = f"INSERT INTO public.pixels(user_id, x_cord, y_cord, color_id, time_placed, id_mod_action, is_top, deleted_at) VALUES('{user_id}', {x_cord}, {y_cord}, {color_id}, '{time_placed}', '{is_mod_action}', '{is_top_pixel}', '{deleted_at}');"
        cur.execute(sql)
        print("line entered")


def add_delete_users_to_db():
    users = [('kyleraykbs@lemmy.ml', 1915), ('nataliathedrowned2@kbin.run', 1916),('toast@feddit.org', 1917),
             ('cypherpunks@lemmy.ml', 1918), ('d00ery@lemmy.world', 1919), ('Ethgar@berlin.social', 1920),
             ('Virual@lemmy.dbzer0.com', 1921), ('eaglesrl@lemmy.blahaj.zone', 1922),
             ('CauseOfBSOD@fedi.bangsparks.com', 1923), ('lea@lea.pet', 1924), ('uplink@programming.dev', 1925),
             ('muekoeff@social.saarland', 1926), ('polar@lemmy.ml', 1927)]
    for user in users:
        sql = f"INSERT INTO public.users(username, ranking, total_pixels_placed) VALUES ('{user[0]}', {user[1]}, 0);"
        cur.execute(sql)
        print("posted")


def add_colors_to_db():
    for color in color_tuples:
        sql = f"INSERT INTO public.colors(color_id, color_name, color_hex) VALUES ({color[0]}, '{color[1]}', '{color[2]}');"
        cur.execute(sql)
        print("posted")


def get_top_cord_for_single_user(user_id):
    sql = f"SELECT x_cord, y_cord FROM public.pixels WHERE user_id={user_id}"
    cur.execute(sql)
    rows = cur.fetchall()
    cords = {}
    for row in rows:
        cord = (row[0], row[1])
        if cord in cords:
            cords[cord] += 1
        else:
            cords[cord] = 1
    highest_cord = (0, 0)
    highest_count = 0
    for cord in cords:
        curr_count = cords[cord]
        if curr_count > highest_count:
            highest_cord = cord
            highest_count = curr_count
    return highest_cord, highest_count


def get_user_id_list():
    sql = "SELECT user_id FROM public.users ORDER BY user_id"
    cur.execute(sql)
    rows = cur.fetchall()
    user_ids = []
    for row in rows:
        user_ids.append(row[0])
    return user_ids


def create_and_dump_top_cord_data():
    user_ids = get_user_id_list()
    for user_id in user_ids:
        cord_and_count = get_top_cord_for_single_user(user_id)
        top_cord = cord_and_count[0]
        x_cord = top_cord[0]
        y_cord = top_cord[1]
        count = cord_and_count[1]
        sql = f"INSERT INTO public.top_cord(user_id, x_cord, y_cord, count_placed) VALUES ({user_id}, {x_cord}, {y_cord}, {count});"
        cur.execute(sql)
        print(f"posted user_id: {user_id}")


create_and_dump_top_cord_data()
conn.commit()
print("Records created successfully")
conn.close()
