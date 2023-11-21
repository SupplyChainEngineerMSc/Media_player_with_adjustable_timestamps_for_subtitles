# Media_player_with_adjustable_timestamps_for_subtitles
Media player with adjustable timestamps for the subtitles.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description

This Python script utilizes the VLC library and Tkinter to create a simple media player with subtitle adjustment and time tracking features. It allows users to play videos, adjust subtitles, jump forward or backward, and tracks the elapsed time.

## Features

- Play/Pause movie
- Adjust subtitles with arrow keys
- Jump forward or backward in 15-second intervals
- Resume playback from a previously stopped position for the specific movie file
- Fullscreen mode
- Time tracking with historical data recorded in `movie_history.txt`

## Installation

1. Clone the repository:

gh repo clone SupplyChainEngineerMSc/Media_player_with_adjustable_timestamps_for_subtitles
https://github.com/SupplyChainEngineerMSc/Media_player_with_adjustable_timestamps_for_subtitles.git

2. Install dependencies:

pip install python-vlc


## Usage
1. Launch the script and select a video file and subtitle file when prompted.

2. Use the following controls:

* Arrow Up/Down: Adjust subtitles by 250 milliseconds
* Arrow Right/Left: Jump forward/backward
* Spacebar/P: Toggle play/pause
* Double-Click/F: Toggle fullscreen
* 'j'/'m': Adjust subtitles by 10 seconds
* 'r': Resume playback from a stopped position


## Contributing
If you'd like to contribute to this project, follow these steps:

* Fork the repository.
* Create a new branch (git checkout -b feature/your-feature).
* Commit your changes (git commit -m 'Add some feature').
* Push to the branch (git push origin feature/your-feature).
* Open a pull request.


## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgements
[python-vlc][https://www.olivieraubert.net/vlc/python-ctypes/]
[tkinter][https://docs.python.org/3/library/tkinter.html]
