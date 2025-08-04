# main.py

import csv
import os
from time import time
from multiprocessing import Pool, cpu_count
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import chess.engine

# --- Our project modules ---
from board import fen_to_2d_board, apply_move
from evaluation import evaluate_board, is_unstable
from minimax import find_best_move_fixed_depth
from selective import find_best_move_selective
from minimax_naive import find_best_move_naive
from arbiter import get_stockfish_evaluation, STOCKFISH_PATH

DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archive', 'chessData.csv')

def get_user_config():
    config = {}
    print("--- Welcome to the Interactive Chess Engine Comparison Tool ---")
    print("This tool will guide you through setting up a simulation.")

    # 1. Get Number of Boards
    print("\n[Step 1: Number of Boards to Test]")
    print("Recommendation: Use 10 for a quick test, use 100 for robust analysis with a credible sample size")
    while True:
        try:
            num = int(input("How many board positions would you like to load? "))
            if num > 0:
                config['num_boards'] = num
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    # 2. Get Search Depths
    print("\n[Step 2: Search Depth for A/B and Selective Engines]")
    print("Depth determines how many moves ahead the AI looks. Runtime grows exponentially with depth.")
    print("Recommendation: Use Depth 2 for a very fast run, Depth 3 for a standard run (minutes), or Depth 4 for a long run (can be 30+ minutes).")
    while True:
        try:
            depth = int(input("Enter the search depth (e.g., 3): "))
            if depth > 0:
                config['fixed_depth'] = depth
                config['selective_depth'] = depth # Having both values be the same is the fairest comparision
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print("\n[Step 3: Optional Naive Minimax Comparison]")
    print("This will run an additional engine that doesn't use Alpha-Beta Pruning, as a comparision of algorithm performance.")
    while True:
        choice = input("Would you like to run this final comparison? (y/n): ").lower()
        if choice in ['y', 'yes']:
            config['run_naive'] = True
            print("\n----------------------------------------------------------------")
            print("!!! WARNING: Naive Minimax is VERY SLOW!")
            print(f"At Depth {config['fixed_depth']}, this last stage can take many times longer than the first phase.")
            if config['fixed_depth'] > 3:
                print("A depth > 3 is NOT RECOMMENDED for the naive comparison.")
            print("It is best to run with a small number of boards (e.g., 5-10).")
            print("----------------------------------------------------------------")
            break
        elif choice in ['n', 'no']:
            config['run_naive'] = False
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
    
    print("\nConfiguration complete. Starting simulation...")
    return config

def load_boards_from_csv(file_path, num_boards_target):
    boards_data = []
    board_id_counter = 0
    print(f"Loading board states from {file_path}...")
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                if len(boards_data) >= num_boards_target: break
                fen_string = row['FEN']
                board_2d = fen_to_2d_board(fen_string)
                player_char = fen_string.split(' ')[1]
                player_to_move = 1 if player_char == 'w' else -1
                boards_data.append({
                    "board_id": board_id_counter, "board_state": board_2d,
                    "player_to_move": player_to_move, "is_unstable": is_unstable(board_2d, player_to_move)
                })
                board_id_counter += 1
    except FileNotFoundError: print(f"Error: Dataset file not found at {file_path}"); exit()
    print(f"Finished loading {len(boards_data)} board states.")
    return boards_data

def get_engine_moves(board_data, fixed_depth_param, selective_depth_param, evaluate_fn_param):
    current_board = board_data["board_state"]
    player_to_move = board_data["player_to_move"]
    start_time_fixed = time()
    fixed_result = find_best_move_fixed_depth(current_board, player_to_move, fixed_depth_param, evaluate_fn_param)
    fixed_runtime = time() - start_time_fixed
    start_time_selective = time()
    selective_result = find_best_move_selective(current_board, player_to_move, selective_depth_param, evaluate_fn_param)
    selective_runtime = time() - start_time_selective
    board_data.update({
        "fixed_best_move": fixed_result["best_move"], "fixed_runtime": fixed_runtime,
        "selective_best_move": selective_result["best_move"], "selective_runtime": selective_runtime
    })
    return board_data

def get_naive_move(board_data, fixed_depth_param, evaluate_fn_param):
    current_board = board_data["board_state"]
    player_to_move = board_data["player_to_move"]
    start_time_naive = time()
    naive_result = find_best_move_naive(current_board, player_to_move, fixed_depth_param, evaluate_fn_param)
    naive_runtime = time() - start_time_naive
    board_data.update({
        "naive_best_move": naive_result["best_move"], "naive_runtime": naive_runtime
    })
    return board_data

def run_simulations_parallel(worker_fn, boards_data, phase_name, *args):
    print(f"\n{phase_name}: Running on {len(boards_data)} boards using {cpu_count()} CPU cores...")
    start_time = time()
    simulation_args = [(d, *args) for d in boards_data]
    with Pool(processes=cpu_count()) as pool:
        results = pool.starmap(worker_fn, simulation_args)
    print(f"{phase_name} complete in {time() - start_time:.2f} seconds.")
    return results

def judge_all_moves_with_stockfish(results):
    print(f"\nJudging {len(results)} results with a persistent Stockfish engine...")
    start_time = time()
    engine = None
    try:
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        for i, r in enumerate(results):
            if r.get("fixed_best_move"):
                board, next_player = apply_move(r["board_state"], r["fixed_best_move"], r["player_to_move"])
                r["fixed_true_score"] = get_stockfish_evaluation(board, next_player, engine)
            if r.get("selective_best_move"):
                board, next_player = apply_move(r["board_state"], r["selective_best_move"], r["player_to_move"])
                r["selective_true_score"] = get_stockfish_evaluation(board, next_player, engine)
            if r.get("naive_best_move"):
                board, next_player = apply_move(r["board_state"], r["naive_best_move"], r["player_to_move"])
                r["naive_true_score"] = get_stockfish_evaluation(board, next_player, engine)
            if (i + 1) % 10 == 0: print(f"  Judged {i + 1}/{len(results)} positions...")
    except chess.engine.EngineTerminatedError as e: print(f"\nFATAL ERROR: Stockfish terminated. {e}")
    finally:
        if engine: engine.quit()
    print(f"Judging complete in {time() - start_time:.2f} seconds.")
    return results

def visualize_selective_comparison(results):
    print("\nCreating Selective vs. Fixed A/B comparison plot...")
    if not results: return
    quality_stable = {'fixed': 0, 'selective': 0, 'equal': 0}
    quality_unstable = {'fixed': 0, 'selective': 0, 'equal': 0}
    for r in results:
        is_unstable_pos = r.get("is_unstable", False)
        fixed_score = r.get("fixed_true_score", 0)
        selective_score = r.get("selective_true_score", 0)
        if r.get("player_to_move") == 1:
            if selective_score > fixed_score: winner = 'selective'
            elif fixed_score > selective_score: winner = 'fixed'
            else: winner = 'equal'
        else:
            if selective_score < fixed_score: winner = 'selective'
            elif fixed_score < selective_score: winner = 'fixed'
            else: winner = 'equal'
        if is_unstable_pos: quality_unstable[winner] += 1
        else: quality_stable[winner] += 1
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Fixed A/B vs. Selective/Quiescent Search (Judged by Stockfish)', fontsize=16)
    total_quality = {'Fixed A/B Better': quality_stable['fixed'] + quality_unstable['fixed'], 'Selective Better': quality_stable['selective'] + quality_unstable['selective'], 'Equal Score': quality_stable['equal'] + quality_unstable['equal']}
    axes[0].bar(total_quality.keys(), total_quality.values(), color=['coral', 'teal', 'grey'])
    axes[0].set_ylabel('Number of Boards')
    axes[0].set_title('Overall Move Quality')
    labels = ['Selective Better', 'Fixed A/B Better', 'Equal Score']
    stable_counts = [quality_stable['selective'], quality_stable['fixed'], quality_stable['equal']]
    unstable_counts = [quality_unstable['selective'], quality_unstable['fixed'], quality_unstable['equal']]
    x = np.arange(len(labels))
    width = 0.35
    axes[1].bar(x - width/2, stable_counts, width, label='Stable Positions', color='coral')
    axes[1].bar(x + width/2, unstable_counts, width, label='Unstable Positions', color='teal')
    axes[1].set_ylabel('Number of Boards')
    axes[1].set_title('Move Quality by Position Stability')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels)
    axes[1].legend()
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('selective_comparison.png')
    print("Selective comparison analysis saved to selective_comparison.png")

def visualize_ab_comparison(results):
    print("\nCreating Alpha-Beta Pruning comparison plot...")
    total_fixed_runtime = sum(r.get("fixed_runtime", 0) for r in results)
    total_naive_runtime = sum(r.get("naive_runtime", 0) for r in results)
    quality = {'ab_better': 0, 'naive_better': 0, 'equal': 0}
    for r in results:
        if r.get("player_to_move") == 1:
            if r.get("fixed_true_score", 0) > r.get("naive_true_score", 0): quality['ab_better'] += 1
            elif r.get("naive_true_score", 0) > r.get("fixed_true_score", 0): quality['naive_better'] += 1
            else: quality['equal'] += 1
        else:
            if r.get("fixed_true_score", 0) < r.get("naive_true_score", 0): quality['ab_better'] += 1
            elif r.get("naive_true_score", 0) < r.get("fixed_true_score", 0): quality['naive_better'] += 1
            else: quality['equal'] += 1
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Alpha-Beta Pruning vs. Naive Minimax Performance', fontsize=16)
    axes[0].bar(['A/B Pruning', 'Naive Minimax'], [total_fixed_runtime, total_naive_runtime], color=['dodgerblue', 'orangered'])
    axes[0].set_ylabel('Total Runtime (seconds)')
    axes[0].set_title('Log Scale Runtime Comparison (Lower is Better)')
    axes[0].set_yscale('log')
    labels = ['A/B Finds Same Move', 'A/B Finds Better Move', 'Naive Finds Better Move']
    counts = [quality['equal'], quality['ab_better'], quality['naive_better']]
    axes[1].bar(labels, counts, color=['limegreen', 'green', 'darkred'])
    axes[1].set_ylabel('Number of Boards')
    axes[1].set_title('Move Quality Comparison')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('ab_pruning_comparison.png')
    print("Pruning comparison analysis saved to ab_pruning_comparison.png")

if __name__ == "__main__":
    start_total_time = time()
    config = get_user_config()
    
    try:
        boards_for_sim = load_boards_from_csv(DATASET_PATH, config['num_boards'])
        if boards_for_sim:
            results_phase1 = run_simulations_parallel(get_engine_moves, boards_for_sim, "Phase 1 (Selective & Fixed A/B)", config['fixed_depth'], config['selective_depth'], evaluate_board)
            judged_results1 = judge_all_moves_with_stockfish(results_phase1)
            if judged_results1:
                visualize_selective_comparison(judged_results1)

            if config['run_naive']:
                print("\n---\nWARNING: Starting Phase 3. This will be significantly slower.")
                print("Running Minimax WITHOUT Alpha-Beta Pruning...")
                results_phase3 = run_simulations_parallel(get_naive_move, judged_results1, "Phase 3 (Naive Minimax)", config['fixed_depth'], evaluate_board)
                final_results = judge_all_moves_with_stockfish(results_phase3)
                if final_results:
                    visualize_ab_comparison(final_results)

    except Exception as e:
        print(f"\nAn unexpected error occurred during the main execution: {e}")
    finally:
        total_runtime = time() - start_total_time
        print(f"\nTotal wall-clock time for entire script: {total_runtime:.2f} seconds.")
        print("--- Simulation Complete ---")
