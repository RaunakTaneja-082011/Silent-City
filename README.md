# Silent-City
A Pygame simulation game where you strategically place barriers and trees to reduce noise pollution across a city grid. Can you bring peace and quiet back to the urban landscape?

🎮 Game Overview
Silent City: dB Down is an engaging simulation game built with Pygame that challenges players to manage and reduce noise levels in a dynamic city environment. The city is represented by a grid, with each cell indicating a specific noise level in decibels (dB). Your mission is to strategically deploy noise-reducing elements like barriers and trees to lower the average noise across the city to an acceptable level, progressing through various challenging levels.

✨ Features
Dynamic Noise Grid: Each cell on the 5x5 grid has a random noise level (50-90 dB).

Strategic Noise Reduction:

Barriers (R key): Reduce noise by 10 dB per placement.

Trees (T key): Reduce noise by 5 dB per placement.

Resource Management: Limited number of barriers and trees per level.

Progressive Levels: Three distinct levels with varying resource allocations and increasing difficulty.

Win/Loss Conditions: Win by reducing average noise below 60 dB; lose if resources run out and noise remains high.

Game State Management: Save and load game progress.

In-game Instructions: Toggleable help menu for easy reference.

Visual Feedback: Cells change color based on noise levels (green for low, yellow for moderate, red for high).

Sound Effects (Optional): Audio cues for cell selection and noise reduction.

🕹️ How to Play
Run the Game: Execute the Python script.

Select a Cell: Click on any cell in the grid to select it. The selected cell will be highlighted.

Reduce Noise:

Press R to place a Barrier on the selected cell (reduces noise by 10 dB). This consumes one barrier resource.

Press T to plant Trees on the selected cell (reduces noise by 5 dB). This consumes one tree resource.

Monitor Noise: Keep an eye on the "Average Noise" display. Your goal is to get it below 60 dB.

Game State Controls:

Press H to toggle Help/Instructions.

Press S to Save your current game progress.

Press L to Load a previously saved game.

Press N to start a New Game or advance to the next level after winning.

🚀 Installation
To run Silent City: dB Down, you'll need Python and Pygame installed.

Clone the repository (or download the source code):

git clone https://github.com/your-username/silent-city-db-down.git
cd silent-city-db-down

(Replace your-username with your actual GitHub username if you fork it)

Install Pygame:
If you don't have Pygame installed, you can install it via pip:

pip install pygame

Optional: Add Sound Assets:
For sound effects, create an assets folder in the same directory as the game script and place select.wav and reduce.wav files inside it.

silent-city-db-down/
├── game_script.py
└── assets/
    ├── select.wav
    └── reduce.wav

▶️ Running the Game
Once Pygame is installed and you have the game script, simply run it from your terminal:

python game_script.py

(Replace game_script.py with the actual name of your Python game file)

📄 License
This project is licensed under the MIT License - see the LICENSE file for details (if you plan to add one).

🙏 Acknowledgements
Built with Pygame.

Sound effects (if used) from [source_name] (e.g., "Freesound.org" or "OpenGameArt.org").
