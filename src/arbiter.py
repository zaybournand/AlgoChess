# arbiter.py

import chess
import chess.engine
import os

STOCKFISH_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stockfish')

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

    active_color = 'w' if player_to_move == 1 else 'b'
    
    fen += f' {active_color} - - 0 1'
    
    return fen

def get_stockfish_evaluation(board_state, player_to_move, engine):
    if not engine:
        return 0

    fen_string = board_to_fen(board_state, player_to_move)
    board = chess.Board(fen_string)

    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    score = info["score"].white().score(mate_score=10000)

    return score
