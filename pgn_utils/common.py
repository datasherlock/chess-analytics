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
        </style>
        <div class="navbar">
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

    st.markdown("""----""")
    _,two,_ =  st.columns(3)
    two.image("https://images.chesscomfiles.com/uploads/v1/images_users/tiny_mce/PedroPinhata/phpNgJfyb.png", width=200)


    # columns = st.columns(8)

    # with columns[2]:
    #     st.write("""<div style="width:100%;text-align:center;"><a href="https://www.jeromerajan.com" style="float:center"><img src="https://cdn0.iconfinder.com/data/icons/england-13/504/sherlock-holmes-detective-inspector-man-512.png" width="22px"></img></a></div>""", unsafe_allow_html=True)

    # with columns[3]:
    #     st.write("""<div style="width:100%;text-align:center;"><a href="https://linkedin.com/in/jeromerajan" style="float:center"><img src="https://cdn2.iconfinder.com/data/icons/social-media-applications/64/social_media_applications_14-linkedin-512.png" width="22px"></img></a></div>""", unsafe_allow_html=True)

    # with columns[4]:
    #     st.write("""<div style="width:100%;text-align:center;"><a href="https://medium.com/@datasherlock" style="float:center"><img src="https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Medium-512.png" width="22px"></img></a></div>""", unsafe_allow_html=True)

    # with columns[5]:
    #     st.write("""<div style="width:100%;text-align:center;"><a href="https://github.com/datasherlock" style="float:center"><img src="https://cdn3.iconfinder.com/data/icons/social-media-2169/24/social_media_social_media_logo_github_2-512.png" width="22px"></img></a></div>""", unsafe_allow_html=True)

    st.markdown("""---""")
    # _, feedback, _ = st.columns(3)
    # feedback.markdown("""Share your feedback at [Github Repo Issues](https://github.com/datasherlock/spark-config-calculator/issues)""")

