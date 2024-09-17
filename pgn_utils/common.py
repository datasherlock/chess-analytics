import re
import streamlit as st


@staticmethod
def strip_whitespace(text):
    lst = text.split('"')
    for i, item in enumerate(lst):
        if not i % 2:
            lst[i] = re.sub(r"\s+", "~", item)
    return '"'.join(lst)


def set_page_header_format():
    st.set_page_config(
        page_title="chess.com PGN to a CSV Convertor",
        page_icon="️:material/chess:",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    st.text("This application helps convert PGNs from chess.com into a structured CSV file")

    st.markdown(
        """
            <style>
                .appview-container .main .block-container {{
                    padding-top: {padding_top}rem;
                    padding-bottom: {padding_bottom}rem;
                    }}

            </style>""".format(
            padding_top=0, padding_bottom=1
        ),
        unsafe_allow_html=True,
    )

    navbar = """
        <style>
            .navbar {
                background-color: #333;
                padding: 10px;
                color: white;
                text-align: center;
                top-margin: 0px;

            }
            .navbar a {
                color: white;
                text-decoration: none;
                padding: 10px;
            }
            .navbar img {
                width: 115px;  /* Adjust width to reduce size */
                height: auto;  /* Maintain aspect ratio */
                vertical-align: top;
                float: left;
                padding-left: 10px;
            }
        </style>
        <div class="navbar">
            <a href="https://www.chess.com/member/datasherlock"><img src="https://images.chesscomfiles.com/uploads/v1/images_users/tiny_mce/PedroPinhata/phpNgJfyb.png" alt="Chess Image" /></a>
            <a href="https://www.jeromerajan.com">About</a>
            <a href="https://linkedin.com/in/jeromerajan">LinkedIn</a>
            <a href="https://medium.com/@datasherlock">Medium</a>
            <a href="https://github.com/datasherlock">Github</a>
            <a href="https://buymeacoffee.com/datasherlock">Buy me a coffee</a>
        </div>
    """
    st.markdown("""<p />""", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; '>Chess PGN to CSV Convertor</h1>", unsafe_allow_html=True)
    st.markdown(navbar, unsafe_allow_html=True)


