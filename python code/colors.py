import re

color_tuples = [(1,'White','FFFFFF'), (2,'Light Grey','B9C3CF'), (3,'Medium Grey','777F8C'), (4,'Deep Grey','424651'), (5,'Dark Grey','1F1E26'), (6,'Black','000000'), (7,'Dark Chocolate','382215'), (8,'Chocolate','7C3F20'), (9,'Brown','C06F37'), (10,'Peach','FEAD6C'), (11,'Beige','FFD2B1'), (12,'Pink','FFA4D0'), (13,'Magenta','F14FB4'), (14,'Mauve','E973FF'), (15,'Purple','A630D2'), (16,'Dark Purple','531D8C'), (17,'Navy','242367'), (18,'Blue','0334BF'), (19,'Azure','149CFF'), (20,'Aqua','8DF5FF'), (21,'Light Teal','01BFA5'), (22,'Dark Teal','16777E'), (23,'Forest','054523'), (24,'Dark Green','18862F'), (25,'Green','61E021'), (26,'Lime','B1FF37'), (27,'Pastel Yellow','FFFFA5'), (28,'Yellow','FDE111'), (29,'Orange','FF9F17'), (30,'Rust','F66E08'), (31,'Maroon','550022'), (32,'Rose','99011A'), (33,'Red','F30F0C'), (34,'Watermelon','FF7872')]

color_dict = {'FFFFFF': 1, 'B9C3CF': 2, '777F8C': 3, '424651': 4, '1F1E26': 5, '000000': 6, '382215': 7, '7C3F20': 8, 'C06F37': 9, 'FEAD6C': 10, 'FFD2B1': 11, 'FFA4D0': 12, 'F14FB4': 13, 'E973FF': 14, 'A630D2': 15, '531D8C': 16, '242367': 17, '0334BF': 18, '149CFF': 19, '8DF5FF': 20, '01BFA5': 21, '16777E': 22, '054523': 23, '18862F': 24, '61E021': 25, 'B1FF37': 26, 'FFFFA5': 27, 'FDE111': 28, 'FF9F17': 29, 'F66E08': 30, '550022': 31, '99011A': 32, 'F30F0C': 33, 'FF7872': 34}


def to_camel_case(input_string):
    # Split the string into words based on spaces, underscores, or hyphens
    words = re.split(r'\s|_|-', input_string)

    # Capitalize the first letter of each word after the first word
    camel_case_string = words[0].lower() + ''.join(word.capitalize() for word in words[1:])

    return camel_case_string


for color in color_tuples:
    color_name = color[1]
    camel_name = to_camel_case(color_name)
    print(f" case {color[0]}: self.{camel_name} = ")
