Chess AI Search Algorithm Comparison

Team Members:
Mohamed Hussein
Zayne Bournand
Dajana Seitllari

Project Overview
This project compares two chess move selection algorithms:

Fixed-Depth Minimax: Searches to a fixed depth in all positions.
Selective Deepening Minimax: Deepens search adaptively only in "unstable" positions (with captures/checks).

We simulate at least 100,000 move evaluations on a public chess dataset and compare both move quality (evaluation scores) and runtime. The goal is to show that selective deepening improves move quality without excessive runtime cost.

Code Structure:
Project3/
├── archive/
│ └── chessData.csv # Dataset file (not included in repo)
├── src/
│ ├── board.py # Chess rules, board, move generation
│ ├── evaluation.py # Board evaluation
│ ├── main.py # Runs simulations & analysis
│ ├── minimax.py # Fixed-depth minimax implementation
│ └── selective.py # Selective deepening minimax implementation
├── README.md
├── simulation_results.csv # Output results from simulations
└── profile_results.prof # Profiling data for performance analysis

Setup Instructions
Prerequisites
Python 3.8 or newer

Clone and Install:
git clone https://github.com/zaybournand/Project3.git
cd Project3
pip install -r requirements.txt
(Note: The core code mainly uses Python standard libraries.)

Data Setup
The chessData.csv dataset (~209 MB) is not included due to GitHub size limits.
Download it from Kaggle - Chess Evaluations by ronakbadhe.
Extract the zip and locate chessData.csv.
Place chessData.csv inside the archive/ folder in your cloned project directory:
Project3/archive/chessData.csv

Running the Simulation
Run:
python3 src/main.py

The script will:
Load chess positions from archive/chessData.csv (default 1000 boards).
Run both Fixed-Depth and Selective Deepening Minimax on each position.
Utilize multiprocessing to speed up computation.
Print runtime and move quality comparisons.
Save detailed results to simulation_results.csv.
Generate and summarize a profiling report in profile_results.prof.

Configuration
Adjust these parameters inside src/main.py as needed:

NUM_BOARDS_TO_LOAD: How many board states to simulate.
FIXED_DEPTH: Search depth for fixed minimax.
SELECTIVE_DEPTH: Base depth for selective deepening (increases in unstable positions).

Analyzing Results
Open simulation_results.csv with Excel, Google Sheets, or Python (pandas, matplotlib).

Use profile_results.prof with Python's pstats module to profile performance:
python3 -m pstats profile_results.prof
