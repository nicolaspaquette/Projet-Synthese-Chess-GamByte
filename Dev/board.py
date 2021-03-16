from square import square

class board():
    def __init__(self):
        self.is_game_over = False
        self.initialize_board()

    def initialize_board(self):
        self.position = []
        self.row = []
        for i in range(8):
            for j in range(8):
                self.row.append(square(i,j))
            self.position.append(self.row)
            self.row = []

        #[0,   1,  2,  3,  4,  5,  6,  7]
        #[8,   9, 10, 11, 12, 13, 14, 15]
        #[16, 17, 18, 19, 20, 21, 22, 23]
        #[24, 25, 26, 27, 28, 29, 30, 31]
        #[32, 33, 34, 35, 36, 37, 38, 39]
        #[40, 41, 42, 43, 44, 45, 46, 47]
        #[48, 49, 50, 51, 52, 53, 54, 55]
        #[56, 57, 58, 59, 60, 61, 62, 63]

        # ex: self.position[4][3] = 35
        # joueur blanc en bas de la matrice, joueur noir en haut


