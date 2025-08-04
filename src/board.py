# --- Constants for piece types and colors ---
EMPTY = ' '
WHITE_PAWN = 'P'
WHITE_KNIGHT = 'N'
WHITE_BISHOP = 'B'
WHITE_ROOK = 'R'
WHITE_QUEEN = 'Q'
WHITE_KING = 'K'

BLACK_PAWN = 'p'
BLACK_KNIGHT = 'n'
BLACK_BISHOP = 'b'
BLACK_ROOK = 'r'
BLACK_QUEEN = 'q'
BLACK_KING = 'k'

# --- Piece sets ---
ALL_PIECES = {
    WHITE_PAWN, WHITE_KNIGHT, WHITE_BISHOP, WHITE_ROOK, WHITE_QUEEN, WHITE_KING,
    BLACK_PAWN, BLACK_KNIGHT, BLACK_BISHOP, BLACK_ROOK, BLACK_QUEEN, BLACK_KING,
    EMPTY
}
WHITE_PIECES = {WHITE_PAWN, WHITE_KNIGHT, WHITE_BISHOP, WHITE_ROOK, WHITE_QUEEN, WHITE_KING}
BLACK_PIECES = {BLACK_PAWN, BLACK_KNIGHT, BLACK_BISHOP, BLACK_ROOK, BLACK_QUEEN, BLACK_KING}

# --- Utility functions for color and piece interpretation ---
def get_piece_color(piece):
    if piece in WHITE_PIECES: return 'white'
    if piece in BLACK_PIECES: return 'black'
    return 'none'

def get_opponent_color_str(color_str):
    return 'black' if color_str == 'white' else 'white'

def player_value_to_color_str(player_to_move):
    return 'white' if player_to_move == 1 else 'black'

# --- Board creation ---
def create_empty_board():
    return [[EMPTY for _ in range(8)] for _ in range(8)]

# --- Test mini board ---
def initialize_mini_board():
    board = create_empty_board()
    board[7][4] = WHITE_KING 
    board[0][4] = BLACK_KING 
    board[6][0] = WHITE_PAWN 
    board[1][0] = BLACK_PAWN 
    board[7][1] = WHITE_KNIGHT 
    board[0][1] = BLACK_KNIGHT 
    board[7][0] = WHITE_ROOK   
    board[0][0] = BLACK_ROOK   
    return board

# --- Board display ---
def print_board(board):
    for r_idx, row in enumerate(board):
        print(f"{8 - r_idx} | {' | '.join(row)} |")
    print("  ---------------------------------")
    print("    a   b   c   d   e   f   g   h")

# --- Position utilities ---
def is_valid_position(pos):
    row, col = pos
    return 0 <= row < 8 and 0 <= col < 8

def get_piece_at(board, pos):
    if not is_valid_position(pos): return None
    row, col = pos
    return board[row][col]

# --- Move application and game flow ---
def apply_move(board_state, move, player_to_move):
    from_pos, to_pos = move
    piece_to_move = get_piece_at(board_state, from_pos)

    new_board_state = [row[:] for row in board_state]  # Deep copy

    new_board_state[to_pos[0]][to_pos[1]] = piece_to_move
    new_board_state[from_pos[0]][from_pos[1]] = EMPTY

    next_player_to_move = -player_to_move  # Switch player

    return new_board_state, next_player_to_move

def is_capture_move(board_state, move):
    _, to_pos = move
    target_piece = get_piece_at(board_state, to_pos)
    return target_piece != EMPTY and target_piece != None

# --- King detection and check evaluation ---
def find_king(board_state, color_str):
    king_piece = WHITE_KING if color_str == 'white' else BLACK_KING
    for r in range(8):
        for c in range(8):
            if board_state[r][c] == king_piece:
                return (r, c)
    return None

def is_king_in_check(board_state, king_color_str):
    king_pos = find_king(board_state, king_color_str)
    if king_pos is None:
        return False

    opponent_player_value = 1 if king_color_str == 'black' else -1
    opponent_attacking_moves = generate_pseudo_legal_moves(board_state, opponent_player_value)

    for from_sq, to_sq in opponent_attacking_moves:
        if to_sq == king_pos:
            return True
    return False

# --- Terminal state detection (checkmate/stalemate) ---
def is_terminal(board_state, player_to_move):
    legal_moves = generate_legal_moves(board_state, player_to_move)

    if not legal_moves:
        king_color_str = player_value_to_color_str(player_to_move)
        if is_king_in_check(board_state, king_color_str):
            return True  # Checkmate
        else:
            return True  # Stalemate
    return False

# --- Legal and pseudo-legal move ---
def generate_legal_moves(board_state, player_to_move):
    legal_moves = []
    pseudo_legal_moves = generate_pseudo_legal_moves(board_state, player_to_move)
    
    current_player_color_str = player_value_to_color_str(player_to_move)

    for move in pseudo_legal_moves:
        temp_board, _ = apply_move(board_state, move, player_to_move)
        
        if not is_king_in_check(temp_board, current_player_color_str):
            legal_moves.append(move)
            
    return legal_moves

def generate_pseudo_legal_moves(board_state, player_to_move):
    pseudo_moves = []
    current_player_color_str = player_value_to_color_str(player_to_move)

    for r in range(8):
        for c in range(8):
            piece = board_state[r][c]
            piece_color_str = get_piece_color(piece)

            if piece_color_str == current_player_color_str:
                from_pos = (r, c)

                # --- Pawn moves ---
                if piece == WHITE_PAWN:
                    if is_valid_position((r-1, c)) and get_piece_at(board_state, (r-1, c)) == EMPTY:
                        pseudo_moves.append((from_pos, (r-1, c)))
                    if is_valid_position((r-1, c-1)) and get_piece_color(get_piece_at(board_state, (r-1, c-1))) == 'black':
                        pseudo_moves.append((from_pos, (r-1, c-1)))
                    if is_valid_position((r-1, c+1)) and get_piece_color(get_piece_at(board_state, (r-1, c+1))) == 'black':
                        pseudo_moves.append((from_pos, (r-1, c+1)))
                elif piece == BLACK_PAWN:
                    if is_valid_position((r+1, c)) and get_piece_at(board_state, (r+1, c)) == EMPTY:
                        pseudo_moves.append((from_pos, (r+1, c)))
                    if is_valid_position((r+1, c-1)) and get_piece_color(get_piece_at(board_state, (r+1, c-1))) == 'white':
                        pseudo_moves.append((from_pos, (r+1, c-1)))
                    if is_valid_position((r+1, c+1)) and get_piece_color(get_piece_at(board_state, (r+1, c+1))) == 'white':
                        pseudo_moves.append((from_pos, (r+1, c+1)))

                # --- King moves ---
                elif piece in (WHITE_KING, BLACK_KING):
                    king_deltas = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
                    for dr, dc in king_deltas:
                        to_r, to_c = r + dr, c + dc
                        if is_valid_position((to_r, to_c)):
                            target_piece_color = get_piece_color(get_piece_at(board_state, (to_r, to_c)))
                            if target_piece_color != current_player_color_str:
                                pseudo_moves.append((from_pos, (to_r, to_c)))

                # --- Queen moves (combines rook + bishop) ---
                elif piece in (WHITE_QUEEN, BLACK_QUEEN):
                    directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
                    for dr, dc in directions:
                        curr_r, curr_c = r + dr, c + dc
                        while is_valid_position((curr_r, curr_c)):
                            target_piece = get_piece_at(board_state, (curr_r, curr_c))
                            target_color = get_piece_color(target_piece)
                            if target_color == current_player_color_str:
                                break
                            pseudo_moves.append((from_pos, (curr_r, curr_c)))
                            if target_color != 'none':
                                break
                            curr_r += dr
                            curr_c += dc

                # --- Knight moves ---
                elif piece in (WHITE_KNIGHT, BLACK_KNIGHT):
                    knight_deltas = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]
                    for dr, dc in knight_deltas:
                        to_r, to_c = r + dr, c + dc
                        if is_valid_position((to_r, to_c)):
                            target_piece = board_state[to_r][to_c]
                            if get_piece_color(target_piece) != current_player_color_str:
                                pseudo_moves.append((from_pos, (to_r, to_c)))

                # --- Rook moves ---
                elif piece in (WHITE_ROOK, BLACK_ROOK):
                    directions = [(-1,0), (1,0), (0,-1), (0,1)]
                    for dr, dc in directions:
                        curr_r, curr_c = r + dr, c + dc
                        while is_valid_position((curr_r, curr_c)):
                            target_piece = board_state[curr_r][curr_c]
                            target_color = get_piece_color(target_piece)
                            if target_color == current_player_color_str:
                                break
                            pseudo_moves.append((from_pos, (curr_r, curr_c)))
                            if target_color != 'none':
                                break
                            curr_r += dr
                            curr_c += dc

                # --- Bishop moves ---
                elif piece in (WHITE_BISHOP, BLACK_BISHOP):
                    directions = [(-1,-1), (-1,1), (1,-1), (1,1)]
                    for dr, dc in directions:
                        curr_r, curr_c = r + dr, c + dc
                        while is_valid_position((curr_r, curr_c)):
                            target_piece = board_state[curr_r][curr_c]
                            target_color = get_piece_color(target_piece)
                            if target_color == current_player_color_str:
                                break
                            pseudo_moves.append((from_pos, (curr_r, curr_c)))
                            if target_color != 'none':
                                break
                            curr_r += dr
                            curr_c += dc
    return pseudo_moves

# --- Convert FEN notation to 2D board array ---
def fen_to_2d_board(fen_string):
    board = []
    parts = fen_string.split(' ')
    board_fen = parts[0]
    
    for rank_str in board_fen.split('/'):
        row = []
        for char in rank_str:
            if char.isdigit():
                for _ in range(int(char)):
                    row.append(EMPTY)
            else:
                row.append(char)
        board.append(row)
    return board

# --- Test board.py only ---
if __name__ == "__main__":
    current_board = initialize_mini_board()
    print("--- Initializing a simplified board with more pieces ---")
    print_board(current_board)

    print("\n--- Testing White Pawn pseudo-moves from a2 (6,0) ---")
    white_pawn_moves = generate_pseudo_legal_moves(current_board, 1)
    pawn_a2_moves = [m for m in white_pawn_moves if m[0] == (6,0)]
    print(f"Pseudo-legal moves for White Pawn at a2: {pawn_a2_moves}")

    print("\n--- Testing White Knight pseudo-moves from b1 (7,1) ---")
    white_knight_moves = [m for m in white_pawn_moves if m[0] == (7,1)]
    print(f"Pseudo-legal moves for White Knight at b1: {white_knight_moves}")

    print("\n--- Setting up a capture scenario for White Pawn ---")
    capture_board = create_empty_board()
    capture_board[6][1] = WHITE_PAWN
    capture_board[5][0] = BLACK_PAWN
    capture_board[7][4] = WHITE_KING
    capture_board[0][4] = BLACK_KING
    print_board(capture_board)
    capture_moves = generate_pseudo_legal_moves(capture_board, 1)
    pawn_b2_capture_moves = [m for m in capture_moves if m[0] == (6,1)]
    print(f"Pseudo-legal moves for White Pawn at b2 (capture): {pawn_b2_capture_moves}")

    print("\n--- Testing `is_capture_move` ---")
    print(f"Is ((6,1), (5,0)) a capture on this board? {is_capture_move(capture_board, ((6,1), (5,0)))}")
    print(f"Is ((6,1), (5,1)) a capture on this board? {is_capture_move(capture_board, ((6,1), (5,1)))}")

    print("\n--- Setting up a check scenario ---")
    check_board = create_empty_board()
    check_board[7][4] = WHITE_KING
    check_board[0][4] = BLACK_KING
    check_board[1][4] = BLACK_QUEEN
    print_board(check_board)
    print(f"Is White King in check? {is_king_in_check(check_board, 'white')}")
    print(f"Is Black King in check? {is_king_in_check(check_board, 'black')}")

    print("\n--- Testing terminal state (simplified checkmate) ---")
    checkmate_board_example = create_empty_board()
    checkmate_board_example[0][0] = BLACK_KING
    checkmate_board_example[1][1] = WHITE_QUEEN
    checkmate_board_example[0][1] = WHITE_QUEEN
    checkmate_board_example[7][7] = WHITE_KING
    print("\n--- Checkmate example (Black King a8, White Queens b7, b8) ---")
    print_board(checkmate_board_example)
    print(f"Is this board terminal for Black? {is_terminal(checkmate_board_example, -1)}")
    
    print(f"Is the initial mini board terminal for White? {is_terminal(initialize_mini_board(), 1)}")
