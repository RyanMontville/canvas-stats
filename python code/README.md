# Pyhton code
Here are some of the oython functions I used for Canvas Stats.

I wanted to build a slightly different database than the sql file posted by the Canvas event developer. His database had all of the data in a single table. I wanted to create a users table so I could create additional tables and join them. I also created a color table to store the color names and hex values. 

I converted the rows from the original sql file into a csv file, then ran some functions to create user IDs and color IDs and then converted the usernames and hex codes to their IDs in the pixels table. The files do not contain all of the code I wrote to help create the multiple versions of the database because I was trying to fix the data quickly and was writing over old code or deleting files to keep the files managable.

I also wrote some functions to create csv files for Canvas stats to load the data, which I found was the easiest free way to get over 700,000 rows of data into the app.