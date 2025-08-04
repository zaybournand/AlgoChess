
from board import apply_move, generate_legal_moves

MATE_SCORE = 100000

def find_best_move_naive(board_state, player_to_move, depth, evaluate_fn):
    best_move = None
    best_score = -float('inf')
    
    legal_moves = generate_legal_moves(board_state, player_to_move)

    for move in legal_moves:
        child_board, next_player = apply_move(board_state, move, player_to_move)
        
        score = -negamax_naive(child_board, next_player, depth - 1, evaluate_fn)

        if score > best_score:
            best_score = score
            best_move = move
        
    return {"best_move": best_move, "score": best_score}

def negamax_naive(board, player_to_move, depth, evaluate_fn):
    legal_moves = generate_legal_moves(board, player_to_move)
    if not legal_moves:
        return -MATE_SCORE

    if depth == 0:
        return player_to_move * evaluate_fn(board)

    max_score = -float('inf')
    for move in legal_moves:
        child_board, next_player = apply_move(board, move, player_to_move)
        score = -negamax_naive(child_board, next_player, depth - 1, evaluate_fn)
        if score > max_score:
            max_score = score
            
    return max_score
