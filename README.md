♟️ Chess Search Algorithm Comparison

👥 Team Members:
Mohamed Hussein
Zayne Bournand
Dajana Seitllari

🧠 Project Overview:

This project compares two chess move selection algorithms:

Fixed-Depth Minimax: Searches all positions to a fixed depth.

Selective Deepening Minimax: Dynamically increases depth in unstable positions (captures/checks).

We simulate over 100,000 move evaluations using a public chess dataset to compare both move quality and runtime. The goal is to demonstrate that selective deepening yields stronger moves without a significant performance cost.

🗂️ Code Structure
Project3/  
├── archive/ # Data folder (not tracked by Git)  
│ └── chessData.csv # Kaggle dataset (user must download)  
├── src/  
│ ├── board.py # ChessBoard class: rules & move generation  
│ ├── evaluation.py # Static board evaluation  
│ ├── main.py # Simulation runner & analyzer  
│ ├── minimax.py # Fixed-depth minimax  
│ └── selective.py # Selective deepening minimax  
├── simulation_results.csv # Results of 1000+ board evaluations  
├── profile_results.prof # Runtime profiling summary  
└── README.md

🛠️ Setup Instructions:

✅ Prerequisites:
Python 3.8 or newer

🔧 Clone & Install

git clone https://github.com/zaybournand/Project3.git

cd Project3

pip install -r requirements.txt

ℹ️ All core code uses Python’s standard libraries. Requirements file is minimal.

📁 Data Setup
Due to GitHub file size limits, the dataset is not included in the repository.

1. Download Dataset
   Kaggle: Chess Evaluations by ronakbadhe

2. Extract File
   Locate and extract chessData.csv from the ZIP archive.

3. Place in Correct Directory
   Project3/archive/chessData.csv

▶️ Running the Simulation

python3 src/main.py

This will:

Load positions from archive/chessData.csv (default: 1000 boards)

Run both algorithms and compare move quality + runtime

Save results to simulation_results.csv

Output runtime stats to profile_results.prof

⚙️ Configuration Options

In src/main.py, you can customize:

NUM_BOARDS_TO_LOAD = 1000

FIXED_DEPTH = 3

SELECTIVE_DEPTH = 2

📊 Analyzing Results:

Simulation Output
Open simulation_results.csv in Excel, Google Sheets, or analyze via Python (pandas, matplotlib, etc.)

Profiling Report

View performance stats:

python3 -m pstats profile_results.prof

📝 Notes:

Multiprocessing is used to parallelize board evaluations for better performance.
Dataset contains pre-evaluated chess board states with move suggestions and scores.
