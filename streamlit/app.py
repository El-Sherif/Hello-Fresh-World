import streamlit as st
import requests
from text_generation import generate_recipe

# Set page config for custom theme
st.set_page_config(
    page_title="Mood-Based Recipe Generator",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.streamlit.io',
        'Report a bug': "https://github.com/streamlit/streamlit/issues",
        'About': "# This is a Mood-Based Recipe Generator App!"
    }
)

# Custom theme
primaryColor = "#00cc66"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#000000"
font = "sans serif"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: {backgroundColor}
    }}
    .sidebar .sidebar-content {{
        background: {secondaryBackgroundColor}
    }}
    .widget-label {{
        color: {textColor};
        font-family: {font};
    }}
    .st-bb {{
        background-color: {primaryColor};
    }}
    .st-at {{
        background-color: {primaryColor};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit UI
def main():
    st.title('Mood-Based Recipe Generator', anchor=None)

    with st.form("recipe_form", clear_on_submit=True):
        st.write("Enter your details to get a personalized recipe:")
        age = st.text_input("Write your age")
        gender = st.text_input("Your gender")
        mood = st.text_input("What do you feel")

        submit_button = st.form_submit_button(label='Get Recipe')

        if submit_button:
            recipe = generate_recipe(age, gender, mood)
            st.success("Here's your personalized recipe:")
            st.write(recipe)

if __name__ == "__main__":
    main()