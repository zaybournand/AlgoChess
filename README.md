♟️ Chess AI Search Algorithm Comparison
👥 Team Members
Mohamed Hussein

Zayne Bournand

Dajana Seitllari

🧠 Project Overview
This project compares two chess move selection algorithms:

Fixed-Depth Minimax: Searches all positions to a fixed depth.

Selective Deepening Minimax: Dynamically increases depth in unstable positions (captures/checks).

We simulate over 100,000 move evaluations using a public chess dataset to compare both move quality and runtime. The goal is to demonstrate that selective deepening yields stronger moves without a significant performance cost.

🗂️ Code Structure
graphql
Copy
Edit
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
🛠️ Setup Instructions
✅ Prerequisites
Python 3.8 or newer

🔧 Clone & Install
bash
Copy
Edit
git clone https://github.com/zaybournand/Project3.git
cd Project3
pip install -r requirements.txt
ℹ️ All core code uses Python's standard libraries. Requirements file is minimal.

📁 Data Setup
Due to GitHub file size limits, the dataset is not included in the repository.

Download Dataset
Kaggle: Chess Evaluations by ronakbadhe

Extract File
Find and extract chessData.csv from the ZIP.

Place in Correct Directory
Move the file to:

bash
Copy
Edit
Project3/archive/chessData.csv
▶️ Running the Simulation
bash
Copy
Edit
python3 src/main.py
This will:

Load positions from archive/chessData.csv (default: 1000 boards)

Run both algorithms and compare move quality + runtime

Save detailed results to simulation_results.csv

Create a profiling report in profile_results.prof

⚙️ Configuration Options
In src/main.py, adjust these variables as needed:

python
Copy
Edit
NUM_BOARDS_TO_LOAD = 1000
FIXED_DEPTH = 3
SELECTIVE_DEPTH = 2
📊 Analyzing Results
Simulation Output:
View simulation_results.csv in Excel, Google Sheets, or Python (e.g., with pandas, matplotlib).

Profiling Report:
View performance metrics using Python’s built-in pstats:

bash
Copy
Edit
python3 -m pstats profile_results.prof
📝 Notes
Multiprocessing is used to speed up simulations.

The dataset contains pre-evaluated chess board states with move suggestions and scores.

This project is for academic exploration of AI search strategies in games.
