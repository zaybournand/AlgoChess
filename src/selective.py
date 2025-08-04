# selective.py

from board import apply_move, generate_legal_moves, is_capture_move

MATE_SCORE = 100000
# The budget for how many captures deep the quiescence search will look.
QUIESCENCE_DEPTH_BUDGET = 4 

def find_best_move_selective(board_state, player_to_move, depth, evaluate_fn):
    best_move = None
    best_score = -float('inf')
    
    alpha = -float('inf')
    beta = float('inf')

    moves = generate_legal_moves(board_state, player_to_move)
    sorted_moves = sorted(moves, key=lambda move: is_capture_move(board_state, move), reverse=True)

    for move in sorted_moves:
        child_board, next_player = apply_move(board_state, move, player_to_move)
        score = -negamax_selective(child_board, next_player, depth - 1, -beta, -alpha, evaluate_fn)

        if score > best_score:
            best_score = score
            best_move = move
        
        alpha = max(alpha, score)

    return {"best_move": best_move, "score": best_score}

def negamax_selective(board, player_to_move, depth, alpha, beta, evaluate_fn):
    legal_moves = generate_legal_moves(board, player_to_move)
    if not legal_moves:
        return -MATE_SCORE

    if depth == 0:
        return quiescence_search(board, player_to_move, QUIESCENCE_DEPTH_BUDGET, alpha, beta, evaluate_fn)

    for move in legal_moves:
        child_board, next_player = apply_move(board, move, player_to_move)
        score = -negamax_selective(child_board, next_player, depth - 1, -beta, -alpha, evaluate_fn)

        if score >= beta:
            return beta
        alpha = max(alpha, score)
        
    return alpha

def quiescence_search(board, player_to_move, depth, alpha, beta, evaluate_fn):
    stand_pat_score = player_to_move * evaluate_fn(board)
    
    if depth == 0:
        return stand_pat_score

    if stand_pat_score >= beta:
        return beta
        
    alpha = max(alpha, stand_pat_score)

    capture_moves = [move for move in generate_legal_moves(board, player_to_move) if is_capture_move(board, move)]

    for move in capture_moves:
        child_board, next_player = apply_move(board, move, player_to_move)
        score = -quiescence_search(child_board, next_player, depth - 1, -beta, -alpha, evaluate_fn)

        if score >= beta:
            return beta
        alpha = max(alpha, score)

    return alpha
