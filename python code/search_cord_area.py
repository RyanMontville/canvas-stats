import psycopg2
from PIL import Image

conn = psycopg2.connect(database="canvas2024", user="postgres", password="password", host="127.0.0.1", port="5432")
cur = conn.cursor()


def hex_to_rgb(hex_code):
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))


def give_me_pixels(top_left, bottom_right):
    upper_limit = top_left[0] - 1
    lower_limit = bottom_right[0] + 1
    left_limit = top_left[1] - 1
    right_limit = bottom_right[1] + 1
    sql = ("SELECT x_cord, y_cord, color_hex FROM public.pixels JOIN colors on pixels.color_id = "
           "colors.color_id WHERE is_top = TRUE;")
    cur.execute(sql)
    rows = cur.fetchall()
    output = open("top_left_pixels.txt", "a")
    for row in rows:
        x_cord = row[0]
        y_cord = row[1]
        color_hex = row[2]
        output.write(f"color: '{color_hex}', x: {x_cord}, y: {y_cord}\n")
    output.close()


def draw_pixel_area_and_print_stats(top_left, bottom_right, file_name):
    upper_limit = top_left[0] - 1
    lower_limit = bottom_right[0] + 1
    left_limit = top_left[1] - 1
    right_limit = bottom_right[1] + 1
    sql = ("SELECT username, x_cord, y_cord, color_hex FROM public.pixel JOIN palette_color on pixel.color_id = "
           "palette_color.color_id JOIN users on pixel.user_id = users.user_id WHERE it_top = TRUE")
    cur.execute(sql)
    rows = cur.fetchall()

    usernames = {}
    pixel_count = 0
    img = Image.new('RGB', (1000, 500), "WHITE")
    for row in rows:
        username = row[0]
        x_cord = row[1]
        y_cord = row[2]
        color_hex = row[3]
        if upper_limit < x_cord < lower_limit and left_limit < y_cord < right_limit:
            if username in usernames:
                usernames[username] += 1
            else:
                usernames[username] = 1
            rgb = hex_to_rgb(color_hex)
            img.putpixel((x_cord, y_cord), rgb)
            pixel_count += 1
    img.save(file_name)
    img.show()
    print(len(usernames))
    print(pixel_count)
    print(usernames)


give_me_pixels((1, 1), (20, 20))
# DO NOT REMOVE
conn.close()
# DO NOT REMOVE
