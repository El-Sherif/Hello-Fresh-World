import streamlit as st
import requests
from text_generation import generate_recipe


# Streamlit UI
def main():
    st.title('Mood-Based Recipe Generator')

    with st.form("recipe_form", clear_on_submit=True):
        st.write("Enter your details to get a personalized recipe:")
        age = st.text_input("write your age")
        gender = st.text_input("your gender")
        mood = st.text_input("what do you feel")


        submit_button = st.form_submit_button(label='Get Recipe')

        if submit_button:
            recipe = generate_recipe(age, gender, mood)
            st.success("Here's your personalized recipe:")
            st.write(recipe)

if __name__ == "__main__":
    main()
