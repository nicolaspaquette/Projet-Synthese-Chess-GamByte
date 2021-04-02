#from https://www.chessprogramming.org/Simplified_Evaluation_Function

bottom_pawn_table = [[0,  0,  0,  0,  0,  0,  0,  0],
                    [50, 50, 50, 50, 50, 50, 50, 50],
                    [10, 10, 20, 30, 30, 20, 10, 10],
                    [5,  5, 10, 25, 25, 10,  5,  5],
                    [0,  0,  0, 20, 20,  0,  0,  0],
                    [5, -5,-10,  0,  0,-10, -5,  5],
                    [5, 10, 10,-20,-20, 10, 10,  5],
                    [0,  0,  0,  0,  0,  0,  0,  0]]

top_pawn_table = bottom_pawn_table[::-1]

bottom_knight_table =   [[-50,-40,-30,-30,-30,-30,-40,-50],
                        [-40,-20,  0,  0,  0,  0,-20,-40],
                        [-30,  0, 10, 15, 15, 10,  0,-30],
                        [-30,  5, 15, 20, 20, 15,  5,-30],
                        [-30,  0, 15, 20, 20, 15,  0,-30],
                        [-30,  5, 10, 15, 15, 10,  5,-30],
                        [-40,-20,  0,  5,  5,  0,-20,-40],
                        [-50,-40,-30,-30,-30,-30,-40,-50]]

top_knight_table = bottom_knight_table[::-1]

bottom_bishop_table =   [[-20,-10,-10,-10,-10,-10,-10,-20],
                        [-10,  0,  0,  0,  0,  0,  0,-10],
                        [-10,  0,  5, 10, 10,  5,  0,-10],
                        [-10,  5,  5, 10, 10,  5,  5,-10],
                        [-10,  0, 10, 10, 10, 10,  0,-10],
                        [-10, 10, 10, 10, 10, 10, 10,-10],
                        [-10,  5,  0,  0,  0,  0,  5,-10],
                        [-20,-10,-10,-10,-10,-10,-10,-20]]

top_bishop_table = bottom_bishop_table[::-1]

bottom_rook_table = [[0,  0,  0,  0,  0,  0,  0,  0],
                    [5, 10, 10, 10, 10, 10, 10,  5],
                    [-5,  0,  0,  0,  0,  0,  0, -5],
                    [-5,  0,  0,  0,  0,  0,  0, -5],
                    [-5,  0,  0,  0,  0,  0,  0, -5],
                    [-5,  0,  0,  0,  0,  0,  0, -5],
                    [-5,  0,  0,  0,  0,  0,  0, -5],
                    [0,  0,  0,  5,  5,  0,  0,  0]]

top_rook_table = bottom_rook_table[::-1]

bottom_queen_table =    [[-20,-10,-10, -5, -5,-10,-10,-20],
                        [-10,  0,  0,  0,  0,  0,  0,-10],
                        [-10,  0,  5,  5,  5,  5,  0,-10],
                        [-5,  0,  5,  5,  5,  5,  0, -5],
                        [0,  0,  5,  5,  5,  5,  0, -5],
                        [-10,  5,  5,  5,  5,  5,  0,-10],
                        [-10,  0,  5,  0,  0,  0,  0,-10],
                        [-20,-10,-10, -5, -5,-10,-10,-20]]
            
top_queen_table = bottom_queen_table[::-1]

bottom_king_middle_game_table =     [[-30,-40,-40,-50,-50,-40,-40,-30],
                                    [-30,-40,-40,-50,-50,-40,-40,-30],
                                    [-30,-40,-40,-50,-50,-40,-40,-30],
                                    [-30,-40,-40,-50,-50,-40,-40,-30],
                                    [-20,-30,-30,-40,-40,-30,-30,-20],
                                    [-10,-20,-20,-20,-20,-20,-20,-10],
                                    [20, 20,  0,  0,  0,  0, 20, 20],
                                    [20, 30, 10,  0,  0, 10, 30, 20]]

top_king_middle_game_table = bottom_king_middle_game_table[::-1]

bottom_king_end_game_table =    [[-50,-40,-30,-20,-20,-30,-40,-50],
                                [-30,-20,-10,  0,  0,-10,-20,-30],
                                [-30,-10, 20, 30, 30, 20,-10,-30],
                                [-30,-10, 30, 40, 40, 30,-10,-30],
                                [-30,-10, 30, 40, 40, 30,-10,-30],
                                [-30,-10, 20, 30, 30, 20,-10,-30],
                                [-30,-30,  0,  0,  0,  0,-30,-30],
                                [-50,-30,-30,-30,-30,-30,-30,-50]]

top_king_end_game_table = bottom_king_end_game_table[::-1]

piece_square_table = {
    "bottom_pawn_table": bottom_pawn_table,
    "top_pawn_table": top_pawn_table,
    "bottom_knight_table": bottom_knight_table,
    "top_knight_table": top_knight_table,
    "bottom_bishop_table": bottom_bishop_table,
    "top_bishop_table": top_bishop_table,
    "bottom_rook_table": bottom_rook_table,
    "top_rook_table": top_rook_table,
    "bottom_queen_table": bottom_queen_table,
    "top_queen_table": top_queen_table,
    "bottom_king_middle_game_table": bottom_king_middle_game_table,
    "top_king_middle_game_table": top_king_middle_game_table,
    "bottom_king_end_game_table": bottom_king_end_game_table,
    "top_king_end_game_table": top_king_end_game_table
}



