from board import apply_move, generate_legal_moves

MATE_SCORE = 100000  # Large value representing checkmate

# Find the best move using a basic Negamax search without pruning
def find_best_move_naive(board_state, player_to_move, depth, evaluate_fn):
    best_move = None
    best_score = -float('inf')
    
    legal_moves = generate_legal_moves(board_state, player_to_move)  # Get all legal moves

    for move in legal_moves:
        # Apply move to get new board and next player
        child_board, next_player = apply_move(board_state, move, player_to_move)
        
        # Recursively evaluate move using Negamax, negate because of opponent's turn
        score = -negamax_naive(child_board, next_player, depth - 1, evaluate_fn)

        # Update best score and move if this move is better
        if score > best_score:
            best_score = score
            best_move = move
        
    return {"best_move": best_move, "score": best_score}

# Basic Negamax recursive search without alpha-beta pruning
def negamax_naive(board, player_to_move, depth, evaluate_fn):
    legal_moves = generate_legal_moves(board, player_to_move)
    
    # If no legal moves, assume checkmate (worst case)
    if not legal_moves:
        return -MATE_SCORE

    # If reached max search depth, evaluate board statically
    if depth == 0:
        return player_to_move * evaluate_fn(board)

    max_score = -float('inf')
    
    # Explore all moves recursively
    for move in legal_moves:
        child_board, next_player = apply_move(board, move, player_to_move)
        
        # Negate score because opponent will try to minimize
        score = -negamax_naive(child_board, next_player, depth - 1, evaluate_fn)
        
        if score > max_score:
            max_score = score
            
    return max_score
