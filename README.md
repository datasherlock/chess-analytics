# Chess PGN to CSV Converter

![PGN to CSV convertor](https://images.chesscomfiles.com/uploads/v1/images_users/tiny_mce/PedroPinhata/phpNgJfyb.png)

## Project Description

This Python project provides a simple and efficient way to convert chess games from PGN (Portable Game Notation) format into a structured CSV file.  This tool is particularly useful for analyzing your chess games from platforms like chess.com. The script downloads your game archives, extracts key information such as date, players, opening moves, and results, and neatly organizes them into a CSV file.

## Features

- **Automated PGN Download:**  Fetches all your games directly from chess.com using your username.
- **Data Extraction:**  Parses PGN files to extract essential game details.
- **Structured CSV Output:** Organizes game information into a user-friendly CSV format.
- **Game Filtering:** Optionally filter games by time control, opponent, or other criteria. (Future Implementation)
- **Easy to Use:**  Simple command-line interface for a seamless experience. (Future Implementation)


## Usage Guide

1. **Run the Streamlit app:**
   ```bash
   streamlit run tabulate_my_games.py
   ```
2. **Enter Your Chess.com Username:** In the app interface, provide your chess.com username.
3. **Click "Process All Games":**  The script will download your PGNs, extract the data, and generate the CSV file.
4. **Download Your CSV:** A download button will appear. Click to save the CSV to your computer. 

## Example Code Snippet (for developers)

```python
from pgn_utils.core import UserProfile, PgnParser

# Example usage
user = UserProfile("your_chess_username")
user.get_pgn()  

parser = PgnParser(user) 
parser.process_pgn_files()
parser.download_tabulated_data() 
```

## Contributing Guidelines

Contributions are welcome!  If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive messages.
4. Push your branch to your forked repository.
5. Submit a pull request to the main repository.

## License Information

This project is licensed under the [MIT License](LICENSE).

## Contact Details

For any questions or feedback, please contact [your email address].
