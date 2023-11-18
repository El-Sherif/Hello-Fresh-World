import openai


def generate_recipe(user_preferences, user_mood, allergies):
    # Your OpenAI API key
    openai.api_key = ''

    # Constructing the prompt
    prompt_text = f"Create a recipe considering the following details:\nUser Preferences: {user_preferences}\nUser Mood: {user_mood}\nAllergies: {allergies}\nRecipe:"

    response = openai.Completion.create(
      engine="text-davinci-003", # Or the latest available model
      prompt=prompt_text,
      temperature=0.7,
      max_tokens=150
    )

    return response.choices[0].text.strip()

# Example usage
user_preferences = "prefers spicy food, loves chicken and pasta"
user_mood = "feeling joyful and energetic"
allergies = "allergic to nuts"

recipe = generate_recipe(user_preferences, user_mood, allergies)
print(recipe)