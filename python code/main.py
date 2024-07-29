import psycopg2
from PIL import Image
from color_obj import Colors

conn = psycopg2.connect(database="canvas2024", user="postgres", password="password", host="127.0.0.1", port="5432")
cur = conn.cursor()


def get_usernames():
    sql = "SELECT username FROM public.users;"
    cur.execute(sql)
    rows = cur.fetchall()
    usernames = []
    for row in rows:
        usernames.append(row[0])
    return usernames


def get_user_id_for_username(username):
    sql = f"SELECT user_id FROM public.users WHERE username='{username}'"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows[0][0]


def count_ranked_users():
    sql = "SELECT count(*) FROM public.users WHERE total_pixels_placed > 0;"
    cur.execute(sql)
    return cur.fetchone()[0]


def count_instances():
    sql = "SELECT SPLIT_PART(username, '@', 2) as instance_name, COUNT(*) FROM public.users GROUP BY instance_name ORDER BY COUNT(*) DESC"
    cur.execute(sql)
    instances = cur.fetchall()
    return len(instances)


def count_total_pixels():
    sql = "SELECT count(*) FROM public.pixels;"
    cur.execute(sql)
    # rows = cur.fetchall()
    return cur.fetchone()[0]


def count_colors_placed():
    sql = "SELECT color_name FROM public.pixels Join colors on pixel.color_id = colors.color_id;"
    cur.execute(sql)
    rows = cur.fetchall()
    color_totals = {}
    for row in rows:
        color = row[0]
        if color in color_totals:
            color_totals[color] += 1
        else:
            color_totals[color] = 1
    return color_totals


def find_most_placed_cord():
    sql = "SELECT '(' || x_cord || ',' || y_cord || ')' as cord FROM public.pixels WHERE is_mod_action = FALSE and time_deleted IS NULL;"
    cur.execute(sql)
    rows = cur.fetchall()
    cords = {}
    for row in rows:
        cord = row[0]
        if cord in cords:
            cords[cord] += 1
        else:
            cords[cord] = 1
    sorted_cord_count = sorted(cords.items(), key=lambda kv: kv[1], reverse=True)
    return sorted_cord_count[0]


def get_users_for_cord(x_cord, y_cord):
    users = {}
    sql = f"SELECT username, count(*) FROM public.pixels JOIN users on users.user_id = pixels.user_id WHERE x_cord = {x_cord} and y_cord = {y_cord} and is_mod_action = FALSE and time_deleted IS NULL GROUP BY username ORDER BY count(*) DESC;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        users[row[0]] = row[1]
    return users


def find_users_for_top_cord():
    top_cord_and_count = find_most_placed_cord()
    top_cord = top_cord_and_count[0].strip("(").strip(")").split(",")
    user_who_placed_on_cord = get_users_for_cord(int(top_cord[0]), int(top_cord[1]))
    for user in user_who_placed_on_cord:
        print(f"{user}: {user_who_placed_on_cord[user]} times")


def get_color_count_for_user(user_id):
    sql = (f"SELECT username, color_id, count(color_id) FROM public.pixels JOIN users on users.user_id = "
           f"pixels.user_id WHERE users.user_id = {user_id}  and time_deleted IS NULL GROUP BY username, color_id")
    cur.execute(sql)
    color_count = {}
    rows = cur.fetchall()
    for row in rows:
        color_count[row[1]] = row[2]
    return rows[0][0], color_count


def hex_to_rgb(hex_code):
    return tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))


def draw_users_pixels(username):
    sql = f"SELECT x_cord, y_cord, color_hex FROM public.pixels JOIN users on pixels.user_id = users.user_id JOIN colors on pixels.color_id = colors.color_id WHERE username='{username}';"
    cur.execute(sql)
    rows = cur.fetchall()

    img = Image.new('RGB', (1000, 500), "WHITE")
    for row in rows:
        x_cord = int(row[0])
        y_cord = int(row[1])
        color = row[2]
        rgb = hex_to_rgb(color)
        img.putpixel((x_cord, y_cord), rgb)
    username_parts = username.split("@")
    file_name = f"{username_parts[0]}.png"
    img.save(file_name)
    img.show()


def draw_pixels_special_where(where_statement, file_name):
    sql = (f"SELECT x_cord, y_cord, color_hex, is_mod_action FROM public.pixels JOIN users on pixels.user_id = users.user_id JOIN "
           f"colors on pixels.color_id = colors.color_id WHERE {where_statement} ORDER BY time_placed ASC;")
    cur.execute(sql)
    rows = cur.fetchall()

    img = Image.new('RGB', (1000, 500), "WHITE")
    # img = Image.new('RGB', (1000, 500))
    mod_placed = False
    for row in rows:
        x_cord = int(row[0])
        y_cord = int(row[1])
        color = row[2]
        is_mod_action = row[3]
        rgb = hex_to_rgb(color)
        img.putpixel((x_cord, y_cord), rgb)
    img.save(file_name)
    img.show()


def draw_reversed_order():
    mod_csv = open("mod-csv.csv", "r")
    sql = f"SELECT x_cord, y_cord, color_hex FROM public.pixels JOIN users on pixels.user_id = users.user_id JOIN colors on pixels.color_id = colors.color_id;"
    cur.execute(sql)
    rows = cur.fetchall()
    img = Image.new('RGB', (1000, 500), "WHITE")
    for row in reversed(rows):
        x_cord = int(row[0])
        y_cord = int(row[1])
        color = row[2]
        rgb = hex_to_rgb(color)
        img.putpixel((x_cord, y_cord), rgb)

    file_name = "reversed.png"
    img.save(file_name)
    img.show()


def draw_all_color_imgs():
    sql = "SELECT color_name FROM colors;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        color = row[0]
        draw_pixels_special_where(f"color_name='{color}'", f"colorimages/{color}.png")


def create_pixels_csv():
    output = open("pixels.csv", "a")
    sql = ("SELECT username, x_cord, y_cord, color_hex FROM public.pixels JOIN colors on colors.color_id = "
           "pixels.color_id JOIN users on users.user_id = pixels.user_id WHERE color_hex <> 'FFFFFF' AND time_deleted IS NULL ORDER BY time_placed ASC")
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        output.write(f"{row[0]},{row[1]},{row[2]},#{row[3].strip('\n')}\n")
    output.close()


def get_user_id_list():
    sql = "SELECT user_id FROM public.users ORDER BY user_id"
    cur.execute(sql)
    rows = cur.fetchall()
    user_ids = []
    for row in rows:
        user_ids.append(row[0])
    return user_ids


def create_color_count_2024():
    output = open("fixed_color_count_2024.csv", "a")
    user_ids = get_user_id_list()
    for user_id in user_ids:
        color_count_for_user = get_color_count_for_user(user_id)
        username = color_count_for_user[0]
        user_colors = Colors(color_count_for_user[1])
        output.write(f"{username},{user_colors.black},{user_colors.darkGrey},{user_colors.deepGrey}"
                     f",{user_colors.mediumGrey}"
                     f",{user_colors.lightGrey},{user_colors.white},{user_colors.beige},{user_colors.peach},{user_colors.brown}"
                     f",{user_colors.chocolate},{user_colors.rust},{user_colors.orange},{user_colors.yellow},"
                     f"{user_colors.pastelYellow},{user_colors.lime},{user_colors.green},{user_colors.darkGreen}"
                     f",{user_colors.forest},{user_colors.darkTeal},{user_colors.lightTeal},{user_colors.aqua}"
                     f",{user_colors.azure},{user_colors.blue},{user_colors.navy},{user_colors.purple},{user_colors.mauve},"
                     f"{user_colors.magenta},{user_colors.pink},{user_colors.watermelon},{user_colors.red},{user_colors.rose},"
                     f"{user_colors.maroon},{user_colors.darkChocolate},{user_colors.darkPurple}\n")
        print(f"{user_id} of 1912")
    output.close()


def create_users_2024():
    output = open("fixed_users_2024.csv", "a")
    sql = (f"SELECT username, ranking, total_pixels_placed, x_cord, y_cord, count_placed FROM public.users JOIN "
           f"top_cord on users.user_id = top_cord.user_id WHERE total_pixels_placed > 0 ORDER BY users.ranking ASC")
    cur.execute(sql)
    color_count = {}
    rows = cur.fetchall()
    for row in rows:
        output.write(f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]}\n")
    output.close()


def count_rows_in_database():
    sql = "SELECT COUNT(*) from public.users;"
    cur.execute(sql)
    return cur.fetchone()[0]


print(count_rows_in_database())
# DO NOT REMOVE
conn.close()
# DO NOT REMOVE
