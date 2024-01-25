# Aryaman Sawhney
# piece.py
# a class that holds the details of a piece


# PIECE CLASS
class Piece:
    def __init__(self, type, color, has_moved=False):
        # contains type of piece and color
        self.type = type
        self.color = color

    # function called to check if another piece is the same
    def __eq__(self, comp):
        # tries to access type and color values, if they're equal then return True, else return False. If there are no type value or no color value, returns false
        try:
            if self.type == comp.type and self.color == comp.color:
                return True
        except:
            return False
        else:
            return False
