from board import apply_move, generate_legal_moves, is_capture_move

MATE_SCORE = 100000  # Arbitrary high value to represent a checkmate situation

# Finds the best move using fixed-depth negamax search
def find_best_move_fixed_depth(board_state, player_to_move, depth, evaluate_fn):
    best_move = None
    best_score = -float('inf')
    alpha = -float('inf')
    beta = float('inf')

    # Generate and sort moves to prioritize captures
    moves = generate_legal_moves(board_state, player_to_move)
    sorted_moves = sorted(moves, key=lambda move: is_capture_move(board_state, move), reverse=True)

    for move in sorted_moves:
        # Apply the move and switch player
        child_board, next_player = apply_move(board_state, move, player_to_move)
        
        # Evaluate the position recursively using negamax
        score = -negamax_fixed(child_board, next_player, depth - 1, -beta, -alpha, evaluate_fn)

        # Update best score and move if needed
        if score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, score)  # Update alpha for pruning

    return {"best_move": best_move, "score": best_score}

# Recursive negamax with alpha-beta pruning
def negamax_fixed(board, player_to_move, depth, alpha, beta, evaluate_fn):
    legal_moves = generate_legal_moves(board, player_to_move)

    # If no moves, return checkmate score
    if not legal_moves:
        return -MATE_SCORE

    # If at depth 0, return static evaluation
    if depth == 0:
        return player_to_move * evaluate_fn(board)

    for move in legal_moves:
        child_board, next_player = apply_move(board, move, player_to_move)
        
        # Negamax recursion: switch sign and players
        score = -negamax_fixed(child_board, next_player, depth - 1, -beta, -alpha, evaluate_fn)

        # Beta cutoff
        if score >= beta:
            return beta

        alpha = max(alpha, score)

    return alpha
