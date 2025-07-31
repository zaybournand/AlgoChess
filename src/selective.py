from time import time
from board import generate_legal_moves, apply_move, is_terminal

# --- Node class for representing search tree ---
class Node:
    def __init__(self, board_state, current_move, depth, player_to_move):
        self.board_state = board_state
        self.current_move = current_move
        self.depth = depth
        self.player_to_move = player_to_move

# --- Selective deepening minimax with additional depth in unstable positions ---
def selective_deepening_minimax(node, current_depth, max_overall_depth, evaluate_fn, is_unstable_fn):
    if current_depth == max_overall_depth or is_terminal(node.board_state, node.player_to_move):
        return evaluate_fn(node.board_state), node.current_move

    maximizing_player = node.player_to_move == 1
    best_score = float('-inf') if maximizing_player else float('inf')
    best_move = None

    moves = generate_legal_moves(node.board_state, node.player_to_move)
    if not moves:
        return evaluate_fn(node.board_state), node.current_move

    for move in moves:
        child_board_state, next_player_to_move = apply_move(node.board_state, move, node.player_to_move)
        child_node = Node(child_board_state, move, node.depth + 1, next_player_to_move)

        # Increase depth if the position is unstable like check, capture, etc.
        deeper_depth_for_child_call = current_depth + 1
        if is_unstable_fn(child_node.board_state, child_node.player_to_move):
            deeper_depth_for_child_call += 2

        deeper_depth_for_child_call = min(deeper_depth_for_child_call, max_overall_depth)

        score, _ = selective_deepening_minimax(child_node, deeper_depth_for_child_call, max_overall_depth, evaluate_fn, is_unstable_fn)

        if maximizing_player:
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move

    # Fallback in case no move is selected
    if best_move is None and moves:
        return best_score, moves[0]
    elif best_move is None and not moves:
        return evaluate_fn(node.board_state), node.current_move

    return best_score, best_move

# Entry point to run selective deepening from a given board state
def run_selective_deepening(start_board, player_to_move, max_overall_depth, evaluate_fn, is_unstable_fn):
    root = Node(start_board, None, 0, player_to_move)
    start_time = time()
    score, best_move = selective_deepening_minimax(root, 0, max_overall_depth, evaluate_fn, is_unstable_fn)
    end_time = time()

    return {
        "best_move": best_move,
        "score": score,
        "runtime_sec": end_time - start_time
    }
