# Canvas 2024 SQL

There was an error with the fediverse-auth on the Canvas site where after a certain point new logins started being logged as all lower case which created duplicates of 59 users and were treated as separate users. I have merged all of the duplicate accounts and rebuild the database. 

The SQL file has 4 tables:
* users (user_id, username, ranking, total_pixels_placed)
* colors (color_id, color_name, color_hex)
* pixels (log_id, user_id, x_cord, y_cord, color_id, time_placed, is_mod_action, is_top, time_deleted)
* top_cord (top_cord_id, user_id, x_cord, y_cord, count_placed)

The users table includes the rank and total pixels placed for each user. Deleted pixels are not counted. There are 13 users who deleted every pixel the placed. They are still ranked, but their total pixel count is 0.

The colors table includes the color ID, name, and hex which when joined with the pixels table can be used to easly select the color name or hex.

The pixels table includes the username, x and y coordinates, color ID, the time the pixel was placed, if the pixel was a moderator placement, if the pixel can be seen in the final image, and the time the pixel was deleted or NULL.

The top_cord table includes the x and y coordiantes for the coordinate each user placed the most pixels on along with the count.

The only data not included here is the pixel color counts for each user. You an find the pixel color counts for a user by selecting:

``SELECT color_name, count(color_name)
FROM public.pixels
JOIN users on users.user_id = pixels.user_id
JOIN colors on colors.color_id = pixels.color_id
WHERE username = <username> AND time_deleted IS NULL
GROUP BY color_name``