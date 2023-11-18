import streamlit as st
import requests

# Function to call OpenAI API
def get_recipe(preferences, mood, allergies):
    # Placeholder for OpenAI API call
    # Replace with actual API call logic
    return "Recipe placeholder"

# Streamlit UI
def main():
    st.title('Mood-Based Recipe Generator')

    with st.form("recipe_form", clear_on_submit=True):
        st.write("Enter your details to get a personalized recipe:")
        user_preferences = st.text_input("Your Food Preferences")
        user_mood = st.text_input("Your Current Mood")
        allergies = st.text_input("Any Allergies")

        submit_button = st.form_submit_button(label='Get Recipe')

        if submit_button:
            recipe = get_recipe(user_preferences, user_mood, allergies)
            st.success("Here's your personalized recipe:")
            st.write(recipe)

if __name__ == "__main__":
    main()
