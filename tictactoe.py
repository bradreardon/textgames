class TicTacToeGame(object):
    def __init__(self):
        self.matrix = [[-1, -1, -1],
                       [-1, -1, -1],
                       [-1, -1, -1]]
    
    def translate_index(self, index):
        if index > 9: raise IndexError
        elif index > 6: row = 2
        elif index > 3: row = 1
        elif index > 0: row = 0
        else: raise IndexError
        
        subtract_map = {
            0: 1,
            1: 4,
            2: 7,
        }
        
        col = index - subtract_map[row]
        return (row, col)
    

class Constants:
    O = 0
    X = 1
    BLANK = -1
