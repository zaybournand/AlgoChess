# evaluation.py

from board import get_piece_color, WHITE_PIECES, BLACK_PIECES, EMPTY, is_capture_move, generate_legal_moves, is_king_in_check

# Piece values for material count
PIECE_VALUES = {
    'P': 100, 'N': 300, 'B': 300, 'R': 500, 'Q': 900, 'K': 0,
    'p': -100, 'n': -300, 'b': -300, 'r': -500, 'q': -900, 'k': 0
}

def evaluate_board(board_state):
    score = 0
    for r in range(8):
        for c in range(8):
            piece = board_state[r][c]
            if piece != EMPTY:
                score += PIECE_VALUES.get(piece, 0) # Use .get with default 0 for safety
    return score

def is_unstable(board_state, player_to_move):
    current_player_color_str = 'white' if player_to_move == 1 else 'black'
    
    # Check for immediate checks
    if is_king_in_check(board_state, current_player_color_str):
        return True

    # Check for immediate captures for the current player
    moves = generate_legal_moves(board_state, player_to_move)
    for move in moves:
        if is_capture_move(board_state, move):
            return True
            
    # Check if opponent can immediately capture a piece of the current player
    # Simulate opponent's turn to check for captures
    opponent_player_to_move = -player_to_move
    opponent_color_str = 'white' if opponent_player_to_move == 1 else 'black'

    opponent_moves = generate_legal_moves(board_state, opponent_player_to_move)
    for move in opponent_moves:
        if is_capture_move(board_state, move):
            # Check if the piece being captured belongs to the 'player_to_move'
            from_pos, to_pos = move
            captured_piece = board_state[to_pos[0]][to_pos[1]]
            if get_piece_color(captured_piece) == current_player_color_str:
                return True

    return False