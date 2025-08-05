# selective.py

from board import apply_move, generate_legal_moves, is_capture_move

MATE_SCORE = 100000 # High score used to represent checkmate
QUIESCENCE_DEPTH_BUDGET = 4 # Max depth for quiescence (capture-only) search

# Select best move using Negamax with selective (quiescence) deepening
def find_best_move_selective(board_state, player_to_move, depth, evaluate_fn):
    best_move = None
    best_score = -float('inf')
    alpha = -float('inf')
    beta = float('inf')
    moves = generate_legal_moves(board_state, player_to_move)

    # Prioritize capture moves first (move ordering for efficiency)
    sorted_moves = sorted(moves, key=lambda move: is_capture_move(board_state, move), reverse=True)

    for move in sorted_moves:
        child_board, next_player = apply_move(board_state, move, player_to_move)
        score = -negamax_selective(child_board, next_player, depth - 1, -beta, -alpha, evaluate_fn)
        if score > best_score:
            best_score = score
            best_move = move
        
        alpha = max(alpha, score)
    return {"best_move": best_move, "score": best_score}

# Negamax search with alpha-beta pruning and selective deepening
def negamax_selective(board, player_to_move, depth, alpha, beta, evaluate_fn):
    legal_moves = generate_legal_moves(board, player_to_move)
    if not legal_moves:
        return -MATE_SCORE # No moves = checkmate or stalemate

    if depth == 0:
        # Depth exhausted, switch to quiescence search
        return quiescence_search(board, player_to_move, QUIESCENCE_DEPTH_BUDGET, alpha, beta, evaluate_fn)

    for move in legal_moves:
        child_board, next_player = apply_move(board, move, player_to_move)
        score = -negamax_selective(child_board, next_player, depth - 1, -beta, -alpha, evaluate_fn)

        if score >= beta:
            return beta
        alpha = max(alpha, score)
        
    return alpha

# Extend search to resolve unstable positions (captures only)
def quiescence_search(board, player_to_move, depth, alpha, beta, evaluate_fn):
    stand_pat_score = player_to_move * evaluate_fn(board)
    
    if depth == 0:
        return stand_pat_score # Reached quiescence depth limit

    if stand_pat_score >= beta:
        return beta # Cutoff if position already too strong
        
    alpha = max(alpha, stand_pat_score)
    # Only explore capture moves for quiescence
    capture_moves = [move for move in generate_legal_moves(board, player_to_move) if is_capture_move(board, move)]

    for move in capture_moves:
        child_board, next_player = apply_move(board, move, player_to_move)
        score = -quiescence_search(child_board, next_player, depth - 1, -beta, -alpha, evaluate_fn)

        if score >= beta:
            return beta # Beta cutoff
        alpha = max(alpha, score)

    return alpha
