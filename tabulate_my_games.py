import streamlit as st

from pgn_utils.common import set_page_header_format
from pgn_utils.core import UserProfile, PgnParser


def main():
    set_page_header_format()
    st.warning("Note: This currently works only for Live Games played on chess.com. Does not support Chess960 and other variants")
    user = st.text_input("**Enter your Chess.com Username**", "datasherlock")


    if st.button("Process all games"):
        user = UserProfile(user)
        user_data = user.get_attr()
        user.get_pgn()

        parser = PgnParser(user_data['user'], user_data['pgn_directory'], user_data['games_list'])
        parser.process_pgn_files()
        parser.remove_pgn_dir()
        parser.download_tabulated_data()

if __name__ == "__main__":
    main()