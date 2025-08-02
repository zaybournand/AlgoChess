# main.py

import csv
import os
from time import time
import cProfile
import pstats
from multiprocessing import Pool, cpu_count
from board import fen_to_2d_board
from evaluation import evaluate_board, is_unstable
from minimax import run_fixed_minimax
from selective import run_selective_deepening

# Configuration (free to change if wanted)
NUM_BOARDS_TO_LOAD = 100
FIXED_DEPTH = 3
SELECTIVE_DEPTH = 3
DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archive', 'chessData.csv')

# Load FEN board states from CSV
def load_boards_from_csv(file_path, num_boards_target):
    boards_data = []
    board_id_counter = 0
    print(f"Loading board states from {file_path}...")

    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                if len(boards_data) >= num_boards_target:
                    break

                fen_string = row['FEN']
                current_board_2d = fen_to_2d_board(fen_string)
                player_char = fen_string.split(' ')[1]
                player_to_move = 1 if player_char == 'w' else -1

                boards_data.append({
                    "board_id": board_id_counter,
                    "board_state": current_board_2d,
                    "player_to_move": player_to_move,
                    "is_unstable": is_unstable(current_board_2d, player_to_move)
                })
                board_id_counter += 1

                if (i + 1) % 10 == 0:
                    print(f"Loaded {i + 1} board states...")

    except FileNotFoundError:
        print(f"Error: Dataset file not found at {file_path}")
        exit()
    except KeyError as e:
        print(f"Missing column in CSV: {e}")
        exit()
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit()

    print(f"Finished loading {len(boards_data)} board states.")
    return boards_data

# Run both algorithms on a single board
def process_single_board_simulation(board_data, fixed_depth, selective_depth, evaluate_fn_param, is_unstable_fn_param):
    board_id = board_data["board_id"]
    current_board = board_data["board_state"]
    player_to_move = board_data["player_to_move"]
    is_unstable_pos = board_data["is_unstable"]

    fixed_result = run_fixed_minimax(current_board, player_to_move, fixed_depth, evaluate_fn_param)
    selective_result = run_selective_deepening(current_board, player_to_move, selective_depth, evaluate_fn_param, is_unstable_fn_param)

    return {
        "board_id": board_id,
        "player_to_move": player_to_move,
        "is_unstable_pos": is_unstable_pos,
        "fixed_best_move": fixed_result["best_move"],
        "fixed_score": fixed_result["score"],
        "fixed_runtime_sec": fixed_result["runtime_sec"],
        "selective_best_move": selective_result["best_move"],
        "selective_score": selective_result["score"],
        "selective_runtime_sec": selective_result["runtime_sec"]
    }

# Parallel simulation for all boards
def run_simulations(boards_data, fixed_depth, selective_depth):
    print(f"\nRunning simulations for {len(boards_data)} boards using {cpu_count()} CPU cores...")
    start_all_sims_time = time()

    num_cores = cpu_count() or 1
    simulation_args = [
        (board_data, fixed_depth, selective_depth, evaluate_board, is_unstable)
        for board_data in boards_data
    ]

    results = []
    with Pool(processes=num_cores) as pool:
        for i, res in enumerate(pool.starmap(process_single_board_simulation, simulation_args)):
            results.append(res)
            if (i + 1) % (len(boards_data) // 10 if len(boards_data) > 100 else 10) == 0:
                print(f"Processed {i + 1} boards...")
            elif (i + 1) == len(boards_data):
                print(f"Processed {i + 1} boards (all done).")

    print(f"Finished all simulations in {time() - start_all_sims_time:.2f} seconds.")
    return results

# Analyze comparison between the two algorithms
def analyze_results(results):
    total_fixed_runtime = sum(r["fixed_runtime_sec"] for r in results)
    total_selective_runtime = sum(r["selective_runtime_sec"] for r in results)

    print("\n--- Simulation Summary ---")
    print(f"Total Boards Simulated: {len(results)}")
    print(f"Total Fixed-Depth Minimax Runtime: {total_fixed_runtime:.4f} seconds")
    print(f"Total Selective Deepening Minimax Runtime: {total_selective_runtime:.4f} seconds")
    print(f"Average Fixed-Depth Runtime: {total_fixed_runtime / len(results):.6f} sec")
    print(f"Average Selective Runtime: {total_selective_runtime / len(results):.6f} sec")

    fixed_better_count = 0
    selective_better_count = 0
    draw_score_count = 0
    selective_better_in_unstable = 0
    unstable_pos_count = 0

    for r in results:
        fixed_score = r["fixed_score"]
        selective_score = r["selective_score"]
        is_unstable_pos = r["is_unstable_pos"]

        if is_unstable_pos:
            unstable_pos_count += 1

        if r["player_to_move"] == 1:
            if selective_score > fixed_score:
                selective_better_count += 1
                if is_unstable_pos:
                    selective_better_in_unstable += 1
            elif fixed_score > selective_score:
                fixed_better_count += 1
            else:
                draw_score_count += 1
        else:
            if selective_score < fixed_score:
                selective_better_count += 1
                if is_unstable_pos:
                    selective_better_in_unstable += 1
            elif fixed_score < selective_score:
                fixed_better_count += 1
            else:
                draw_score_count += 1

    print("\n--- Move Quality Comparison ---")
    print(f"Selective better: {selective_better_count}")
    print(f"Fixed better: {fixed_better_count}")
    print(f"Equal: {draw_score_count}")

    print(f"\n--- Unstable Position Analysis ---")
    print(f"Unstable positions: {unstable_pos_count}")
    if unstable_pos_count:
        print(f"Selective better in unstable: {selective_better_in_unstable} ({selective_better_in_unstable / unstable_pos_count:.2%})")
    else:
        print("No unstable positions analyzed.")

# Final results to CSV
def save_results_to_csv(results, filename="simulation_results.csv"):
    if not results:
        print("No results to save.")
        return

    ordered_keys = [
        "board_id", "player_to_move", "is_unstable_pos",
        "fixed_best_move", "fixed_score", "fixed_runtime_sec",
        "selective_best_move", "selective_score", "selective_runtime_sec"
    ]

    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=ordered_keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

    print(f"\nResults saved to {filename}")

# --- Main execution ---
if __name__ == "__main__":
    print("Starting chess Algo simulation project...")

    profiler = cProfile.Profile()
    profiler.enable()

    try:
        print("Step 1: Loading board positions...")
        boards_for_sim = load_boards_from_csv(DATASET_PATH, NUM_BOARDS_TO_LOAD)

        print("Step 2: Running simulations...")
        simulation_results = run_simulations(boards_for_sim, FIXED_DEPTH, SELECTIVE_DEPTH)

        print("Step 3: Analyzing results...")
        analyze_results(simulation_results)

        save_results_to_csv(simulation_results)

    finally:
        profiler.disable()
        stats_filename = "profile_results.prof"
        profiler.dump_stats(stats_filename)
        print(f"\nProfiling data saved to {stats_filename}")
        print("\n--- Top 20 Cumulative Time Functions ---")
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumtime')
        stats.print_stats(20)

    print("\n--- Simulation Complete ---")
