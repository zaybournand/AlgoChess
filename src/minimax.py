import time
from board import apply_move, is_terminal, generate_legal_moves

# --- Node class for representing minimax tree ---
class Node:
    def __init__(self, board_state, current_move, depth, player_to_move):
        self.board_state = board_state         
        self.current_move = current_move       # Move taken to reach this node
        self.depth = depth                     
        self.player_to_move = player_to_move   # 1 for white, -1 for black

# --- Recursive fixed-depth minimax algorithm ---
def fixed_depth_minimax(node, depth, evaluate_fn):
    # Base case: reached max depth or game over
    if depth == 0 or is_terminal(node.board_state, node.player_to_move):
        return evaluate_fn(node.board_state), node.current_move

    maximizing_player = node.player_to_move == 1
    best_score = float('-inf') if maximizing_player else float('inf')
    best_move = None

    moves = generate_legal_moves(node.board_state, node.player_to_move)

    if not moves:
        return evaluate_fn(node.board_state), node.current_move

    for move in moves:
        # Apply move and create child node
        child_board_state, next_player_to_move = apply_move(node.board_state, move, node.player_to_move)
        child_node = Node(child_board_state, move, node.depth + 1, next_player_to_move)

        score, _ = fixed_depth_minimax(child_node, depth - 1, evaluate_fn)

        # Update best score/move depending on player type
        if maximizing_player:
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move
    
    # Fallback if no move found
    if best_move is None and moves:
        return best_score, moves[0]
    elif best_move is None and not moves:
        return evaluate_fn(node.board_state), node.current_move

    return best_score, best_move

# --- Executes the fixed-depth minimax algorithm from a given starting board ---
def run_fixed_minimax(start_board, player_to_move, depth, evaluate_fn):
    root = Node(start_board, None, 0, player_to_move)
    start_time = time.time()
    score, best_move = fixed_depth_minimax(root, depth, evaluate_fn)
    end_time = time.time()

    return {
        "best_move": best_move,          # Best move found at root
        "score": score,                  # Score of best move
        "runtime_sec": end_time - start_time  
    }
