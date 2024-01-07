#PIECE CLASS
class Piece:
  def __init__(self, type, color, has_moved = False):
    #contains type of piece and color
    self.type = type
    self.color = color