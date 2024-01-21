# PIECE CLASS
class Piece:
    def __init__(self, type, color, has_moved=False):
        # contains type of piece and color
        self.type = type
        self.color = color

    def __eq__(self, comp):
        try:
            if self.type == comp.type and self.color == comp.color:
                return True
        except:
            return False
        else:
            return False
