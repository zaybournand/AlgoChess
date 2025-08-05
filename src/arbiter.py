# arbiter.py

import chess
import chess.engine
import os

# Define the path to the Stockfish engine executable
STOCKFISH_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stockfish')

# Convert 2D board state and player to FEN string
def board_to_fen(board_state, player_to_move):
    fen = ""
    for r in range(8):
        empty = 0
        for c in range(8):
            piece = board_state[r][c]
            if piece == ' ':
                empty += 1
            else:
                if empty > 0: fen += str(empty); empty = 0
                fen += piece
        if empty > 0: fen += str(empty)
        if r < 7: fen += '/'

    # Set active color based on player (1 = white, 2 = black)
    active_color = 'w' if player_to_move == 1 else 'b'

     # Add remaining FEN fields (castling, en passant, halfmove, fullmove)
    fen += f' {active_color} - - 0 1'
    return fen

# Evaluate the board position using Stockfish
def get_stockfish_evaluation(board_state, player_to_move, engine):
    if not engine:
        return 0

    fen_string = board_to_fen(board_state, player_to_move)
    board = chess.Board(fen_string)

    # Let Stockfish analyze the board for a short time (0.1 sec)
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    
    # Get centipawn score from white's perspective
    score = info["score"].white().score(mate_score=10000)

    return score
