class Colors:
    def __init__(self, count_dict):
        self.white = 0
        self.lightGrey = 0
        self.mediumGrey = 0
        self.deepGrey = 0
        self.darkGrey = 0
        self.black = 0
        self.darkChocolate = 0
        self.chocolate = 0
        self.brown = 0
        self.peach = 0
        self.beige = 0
        self.pink = 0
        self.magenta = 0
        self.mauve = 0
        self.purple = 0
        self.darkPurple = 0
        self.navy = 0
        self.blue = 0
        self.azure = 0
        self.aqua = 0
        self.lightTeal = 0
        self.darkTeal = 0
        self.forest = 0
        self.darkGreen = 0
        self.green = 0
        self.lime = 0
        self.pastelYellow = 0
        self.yellow = 0
        self.orange = 0
        self.rust = 0
        self.maroon = 0
        self.rose = 0
        self.red = 0
        self.watermelon = 0
        self.set_color_counts(count_dict)

    def set_color_counts(self, color_dict):
        for color in color_dict:
            match color:
                case 1: 
                    self.white = color_dict[color]
                case 2: 
                    self.lightGrey = color_dict[color]
                case 3: 
                    self.mediumGrey = color_dict[color]
                case 4: 
                    self.deepGrey = color_dict[color]
                case 5: 
                    self.darkGrey = color_dict[color]
                case 6: 
                    self.black = color_dict[color]
                case 7: 
                    self.darkChocolate = color_dict[color]
                case 8: 
                    self.chocolate = color_dict[color]
                case 9: 
                    self.brown = color_dict[color]
                case 10: 
                    self.peach = color_dict[color]
                case 11: 
                    self.beige = color_dict[color]
                case 12: 
                    self.pink = color_dict[color]
                case 13: 
                    self.magenta = color_dict[color]
                case 14: 
                    self.mauve = color_dict[color]
                case 15: 
                    self.purple = color_dict[color]
                case 16: 
                    self.darkPurple = color_dict[color]
                case 17: 
                    self.navy = color_dict[color]
                case 18: 
                    self.blue = color_dict[color]
                case 19: 
                    self.azure = color_dict[color]
                case 20: 
                    self.aqua = color_dict[color]
                case 21: 
                    self.lightTeal = color_dict[color]
                case 22: 
                    self.darkTeal = color_dict[color]
                case 23: 
                    self.forest = color_dict[color]
                case 24: 
                    self.darkGreen = color_dict[color]
                case 25: 
                    self.green = color_dict[color]
                case 26: 
                    self.lime = color_dict[color]
                case 27: 
                    self.pastelYellow = color_dict[color]
                case 28: 
                    self.yellow = color_dict[color]
                case 29: 
                    self.orange = color_dict[color]
                case 30: 
                    self.rust = color_dict[color]
                case 31: 
                    self.maroon = color_dict[color]
                case 32: 
                    self.rose = color_dict[color]
                case 33: 
                    self.red = color_dict[color]
                case 34: 
                    self.watermelon = color_dict[color]