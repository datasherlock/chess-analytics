#!/usr/bin/env python
# coding: utf-8

import os
import json
import shutil

import requests
import urllib.request
import pandas as pd
from pathlib import Path
import streamlit as st

from pgn_utils.common import strip_whitespace
from pgn_utils.configs import MOVE_START_LINE, PGN_META, PGN_TEMP_DIRECTORY, EXCLUDE_LIST


class UserProfile:
    def __init__(self, user):
        self.pgn_directory = os.path.join(PGN_TEMP_DIRECTORY,user,"pgn/")
        self.games_list = os.path.join(PGN_TEMP_DIRECTORY, user, "games.csv")
        self.user = user


    def get_attr(self):
        obj_keys = ['user', 'pgn_directory', 'games_list']
        user_data = dict(zip(obj_keys, [self.user, self.pgn_directory, self.games_list]))
        return user_data

    def get_pgn(self):
        """Downloads all the PGNs for a user from chess.com API"""
        with st.status(f"""Getting all games for {self.user}"""):
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
            pgn_archive_links = requests.get(f"https://api.chess.com/pub/player/{self.user}/games/archives", verify=False, headers=headers)
            if not os.path.exists(self.pgn_directory):
                os.makedirs(self.pgn_directory)

            for url in json.loads(pgn_archive_links.content)["archives"]:
                filepath = f"{self.pgn_directory}/{url.split('/')[-2]}{url.split('/')[-1]}.pgn"
                if not Path(filepath).is_file():
                    urllib.request.urlretrieve(f"{url}/pgn", filepath)



class PgnParser:
    def __init__(self, user, pgn_dir, games_list):
        self.pgn_directory = pgn_dir
        self.games_list = games_list
        self.move_start_line = MOVE_START_LINE
        self.pgn_meta = PGN_META
        self.user = user

    def _import_pgn_data(self, filepath):
        """Reads PGN data from a file"""
        with open(filepath) as f:
            for line in f:
                yield line

    def _get_edge_points(self, data):
        """Returns start and end indices for each game in the PGN"""
        starts, ends = [], []
        for n, l in enumerate(data):
            if l.startswith("[Event"):
                if n != 0:
                    ends.append(n - 1)
                starts.append(n)
            elif n == len(data) - 1:
                ends.append(n)
        return starts, ends

    def _group_games(self, data, starts, ends):
        """Groups games into individual lists based on the start and end indices"""
        return (data[starts[i]:ends[i] + 1] for i in range(len(ends)))

    def _merge_moves(self, game):
        """Cleans out the moves and formats the game list"""
        for n, each_row in enumerate(game):
            game[n] = each_row.replace('\n', '')
            if n <= self.move_start_line - 2:
                try:
                    game[n] = strip_whitespace(game[n]).split('~')[1].strip(']["')
                except IndexError as e:
                    continue
        return list(filter(None, game))


    def _create_game_dict(self, games):
        """Creates a dictionary representation of each game"""
        all_games = []
        for each_game in games:
            game_dict = dict(zip(self.pgn_meta, each_game))
            game_dict["whitemoves"], game_dict["blackmoves"] = [], []
            color = "white"

            if any(element.lower() in game_dict["Event"].lower() for element in EXCLUDE_LIST):
                #st.write(each_game)
                pass
            elif game_dict["Event"] == "Let's Play!":
                all_games.append(self._process_lets_play(game_dict))
            else:
                all_games.append(self._process_live_chess(game_dict))

        return all_games

    def _process_lets_play(self, game_dict):
        """Processes 'Let's Play' chess events"""
        for n, move in enumerate(game_dict["Moves"].split(" ")):
            if n % 3 == 0:
                if move in ['1-0', '0-1', '1/2-1/2']:
                    continue
            elif n == (n // 3) + 2:
                if move not in ['1-0', '0-1', '1/2-1/2']:
                    game_dict["whitemoves"].append(move)
            else:
                if move not in ['1-0', '0-1', '1/2-1/2']:
                    game_dict["blackmoves"].append(move)

        self._balance_moves(game_dict)
        del game_dict["Moves"]
        return game_dict

    def _process_live_chess(self, game_dict):
        """Processes Live Chess events"""
        try:
            for move in game_dict["Moves"].split(" "):
                if '{' in move or '}' in move:
                    continue
                elif '.' in move:
                    move_num = int(move.split(".")[0])
                    color = 'black' if "..." in move else "white"
                else:
                    # st.write(f"appending...{move}")
                    self._append_move(game_dict, color, move)

            self._balance_moves(game_dict)
            # st.write("deleting...")
            del game_dict["Moves"]
        except Exception as e:
            pass
            # st.error(f"Error processing game: {e} in {game_dict}")
        return game_dict

    def _append_move(self, game_dict, color, move):
        """Appends move to either white or black moves list"""
        if move not in ['1-0', '0-1', '1/2-1/2']:
            if color == "white":
                game_dict["whitemoves"].append(move)
            else:
                game_dict["blackmoves"].append(move)

    def _balance_moves(self, game_dict):
        """Ensures white and black have the same number of moves"""
        if len(game_dict["blackmoves"]) > len(game_dict["whitemoves"]):
            game_dict["whitemoves"].append("over")
        elif len(game_dict["blackmoves"]) < len(game_dict["whitemoves"]):
            game_dict["blackmoves"].append("over")

    def _explode_moves(self, df):
        """Explode the whitemoves and blackmoves lists into individual rows"""
        # We will create a new DataFrame to hold the expanded rows
        expanded_rows = []

        # Iterate over each row of the DataFrame
        for index, row in df.iterrows():
            # Get the whitemoves and blackmoves for the current row
            whitemoves = row['whitemoves']
            blackmoves = row['blackmoves']

            # Find the maximum number of moves between white and black
            max_moves = max(len(whitemoves), len(blackmoves))

            # Create individual rows for each move pair
            for i in range(max_moves):
                # Create a new row that copies all the metadata from the current game
                new_row = row.copy()

                # Assign white_move and black_move for this row
                new_row['white_move'] = whitemoves[i] if i < len(whitemoves) else None
                new_row['black_move'] = blackmoves[i] if i < len(blackmoves) else None

                # Add the new row to the list of expanded rows
                expanded_rows.append(new_row)

        # Convert the list of expanded rows into a new DataFrame
        expanded_df = pd.DataFrame(expanded_rows)

        # Remove the original whitemoves and blackmoves columns
        final_df = expanded_df.drop(columns=['whitemoves', 'blackmoves'], axis=1, errors="ignore")

        return final_df

    def process_pgn_files(self):
        """Processes PGN files and exports data to CSV"""

        tgt_file = Path(self.games_list)
        tgt_file.unlink(missing_ok=True)
        with st.status(f"Processing all your games..."):
            with os.scandir(self.pgn_directory) as pgn_dir:
                for file in pgn_dir:
                    # st.write(f"Processing file: {file.name}")
                    data = list(self._import_pgn_data(file.path))
                    starts, ends = self._get_edge_points(data)
                    games = self._group_games(data, starts, ends)
                    games = list(map(self._merge_moves, games))
                    all_games = self._create_game_dict(games)

                    for game_dict in all_games:
                        df = self._explode_moves(pd.DataFrame([game_dict]))
                        with open(self.games_list, 'a') as f:
                            df.to_csv(f, mode='a', header=f.tell() == 0, index=False)
        st.success("Export Complete!")


    def remove_pgn_dir(self):
        shutil.rmtree(self.pgn_directory)

    @st.fragment
    def download_tabulated_data(self):
        with open(self.games_list, "rb") as file:
                st.download_button(
                    label="Download CSV",
                    data=file,
                    file_name=f"{self.user}_games.csv",
                    mime="text/csv",
                )
