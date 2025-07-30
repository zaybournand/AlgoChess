# minimax.py

import time
from board import apply_move, is_terminal, generate_legal_moves

class Node:
    def __init__(self, board_state, current_move, depth, player_to_move):
        self.board_state = board_state
        self.current_move = current_move
        self.depth = depth
        self.player_to_move = player_to_move

def fixed_depth_minimax(node, depth, evaluate_fn):
    if depth == 0 or is_terminal(node.board_state, node.player_to_move):
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

        score, _ = fixed_depth_minimax(child_node, depth - 1, evaluate_fn)

        if maximizing_player:
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move
    
    if best_move is None and moves:
        return best_score, moves[0]
    elif best_move is None and not moves:
        return evaluate_fn(node.board_state), node.current_move

    return best_score, best_move

def run_fixed_minimax(start_board, player_to_move, depth, evaluate_fn):
    root = Node(start_board, None, 0, player_to_move)
    start_time = time.time()
    score, best_move = fixed_depth_minimax(root, depth, evaluate_fn)
    end_time = time.time()

    return {
        "best_move": best_move,
        "score": score,
        "runtime_sec": end_time - start_time
    }
