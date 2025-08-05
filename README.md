♟️ Chess Search Algorithm Comparison

👥 Team Members:
Mohamed Hussein
Zayne Bournand
Dajana Seitllari

📽️ Project Demo Video:

Watch our 5-minute demo here: [YouTube Demo](https://youtu.be/VMxQ0dJ5iD0)

🧠 Project Overview:

This project compares two chess move selection algorithms:

Fixed-Depth Minimax with Alpha-Beta Pruning: Searches all positions to a fixed depth.

Selective Deepening Minimax with Alpha-Beta Pruning: Dynamically increases depth in unstable positions (captures/checks).

It futher compares Fixed-Depth Minimax with Alpha-Beta Pruning to a Naive Fixed-Depth Minimax Algorithm, on the basis of runtime and move quality (as judged by Stockfish Chess Engine)

We simulate over 100,000 move evaluations using a public chess dataset to compare both move quality and runtime. The goal is to demonstrate that selective deepening yields stronger moves without a significant performance cost.

🗂️ Code Structure
Project3/  
├── archive/ # Data folder (not tracked by Git)  
│ └── chessData.csv # Kaggle dataset (user must download)  
├── src/  
│ ├── stockfish # Stockfish binary. (user must download)
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

ℹ️ Required modules include the python chess module, matplotlib for visualization, and others, all listed in requirements.txt

📁 Data Setup
Due to GitHub file size limits, the dataset is not included in the repository.

1. Download Dataset
   Kaggle: Chess Evaluations by ronakbadhe

2. Extract File
   Locate and extract chessData.csv from the ZIP archive.

3. Place in Correct Directory
   Project3/archive/chessData.csv

♟️Engine Setup
Due to Github file size limits, the engine binary is not included in the repository.

1. Download stockfish binary for Ubuntu

2. Extract the binary from the .tar file into the same directory as main.py

▶️ Running the Simulation
Navigate to root directory of the project

Run:

python3 src/main.py

This will:

Load positions from archive/chessData.csv (default: 1000 boards)

Run both algorithms and compare move quality + runtime

Save results to simulation_results.csv

Output runtime stats to profile_results.prof

⚙️ Configuration Options

As the script runs, you can specify the search depth (the same depth will be used for fixed search and further recursive quiscence search), the number of boards to load, and whether or not you want to run a naive minimax engine after to compare it to the minimax engine with alpha-beta pruning.
The program output has recommendations for what configurations you should use depending on how long you would like the run to take.

📊 Analyzing Results:

Simulation Output
Open simulation_results.csv in Excel, Google Sheets, or analyze via Python (pandas, matplotlib, etc.)

Profiling Report

View performance stats:

python3 -m pstats profile_results.prof

Visuals are available in:

selective_comparision.png
simulation_analysis.png
ab_pruning_comparision.png

These will be available in the directory you run in. It is best to run in the root directory using the command:

python3 src/main.py

📝 Notes:

Multiprocessing is used to parallelize board evaluations for better performance.
Dataset contains pre-evaluated chess board states with move suggestions and scores.
